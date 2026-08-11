import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient

import app.models.category
from app.models.post import Post
from app.schemas.post import PostResponse
from app.services.post import PostService
from app.main import app


class DummyRedis:
    def __init__(self):
        self.store = {}

    async def get(self, key: str):
        return self.store.get(key)

    async def set(self, key: str, value: str, ex: int = None):
        self.store[key] = value

    async def close(self):
        pass


@pytest.fixture
def sample_posts():
    return [
        Post(
            id=1,
            title="Post 1",
            title_translate="Post 1",
            description="Description 1",
            des="Content 1",
            des_translate="Content 1",
            portrait_image="p1.jpg",
            image="img1.jpg",
            video=None,
            link=None,
            categories="News",
            categories_id=1,
            social_media="@post1",
            views=500,
            date="2026-08-11",
            comment_count=10,
        ),
        Post(
            id=2,
            title="Post 2",
            title_translate="Post 2",
            description="Description 2",
            des="Content 2",
            des_translate="Content 2",
            portrait_image="p2.jpg",
            image="img2.jpg",
            video=None,
            link=None,
            categories="Music",
            categories_id=2,
            social_media="@post2",
            views=300,
            date="2026-08-10",
            comment_count=5,
        ),
    ]


@pytest.mark.asyncio
async def test_get_trending_posts_cache_hit_and_miss(sample_posts):
    mock_repo = MagicMock()
    mock_repo.get_trending.return_value = sample_posts

    dummy_redis = DummyRedis()
    service = PostService(mock_repo)

    with patch("app.core.cache.get_redis_client", return_value=dummy_redis):
        # 1. First call - Cache Miss
        res1 = await service.get_trending_posts(limit=10)
        assert len(res1) == 2
        assert res1[0].id == 1
        assert mock_repo.get_trending.call_count == 1
        assert "trending_posts:10" in dummy_redis.store

        # 2. Second call - Cache Hit
        res2 = await service.get_trending_posts(limit=10)
        assert len(res2) == 2
        assert res2[0].id == 1
        # repo should NOT have been called a second time
        assert mock_repo.get_trending.call_count == 1


@pytest.mark.asyncio
async def test_get_trending_posts_different_limits(sample_posts):
    mock_repo = MagicMock()
    mock_repo.get_trending.return_value = sample_posts

    dummy_redis = DummyRedis()
    service = PostService(mock_repo)

    with patch("app.core.cache.get_redis_client", return_value=dummy_redis):
        await service.get_trending_posts(limit=5)
        await service.get_trending_posts(limit=10)

        assert "trending_posts:5" in dummy_redis.store
        assert "trending_posts:10" in dummy_redis.store
        assert mock_repo.get_trending.call_count == 2


@pytest.mark.asyncio
async def test_get_trending_posts_redis_none_fallback(sample_posts):
    mock_repo = MagicMock()
    mock_repo.get_trending.return_value = sample_posts

    service = PostService(mock_repo)

    with patch("app.core.cache.get_redis_client", return_value=None):
        res = await service.get_trending_posts(limit=10)
        assert len(res) == 2
        assert mock_repo.get_trending.call_count == 1


def test_trending_posts_api_endpoint(sample_posts):
    mock_service = MagicMock()
    mock_service.get_trending_posts = AsyncMock(
        return_value=[PostResponse.model_validate(p, from_attributes=True) for p in sample_posts]
    )

    with patch("app.api.v1.post.get_post_service", return_value=mock_service):
        client = TestClient(app)
        response = client.get("/api/v1/user_web/trending?limit=10")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Post 1"
        assert data[1]["title"] == "Post 2"
