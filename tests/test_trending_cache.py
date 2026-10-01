import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.services.post import PostService
from app.schemas.post import PostResponse
from app.models.post import Post

def create_mock_post(post_id: int, title: str, views: int):
    post = MagicMock(spec=Post)
    post.id = post_id
    post.title = title
    post.title_translate = f"{title} trans"
    post.description = "description"
    post.des = "des"
    post.des_translate = "des trans"
    post.portrait_image = "portrait.jpg"
    post.image = "image.jpg"
    post.video = None
    post.link = None
    post.categories = "Music"
    post.categories_id = 1
    post.social_media = "Twitter"
    post.views = views
    post.date = "2026-08-11"
    post.comment_count = 0
    return post

@pytest.mark.asyncio
async def test_get_trending_posts_cache_miss_and_hit():
    mock_repo = MagicMock()
    mock_posts = [
        create_mock_post(1, "Trending Post 1", 100),
        create_mock_post(2, "Trending Post 2", 80),
    ]
    mock_repo.get_trending.return_value = mock_posts

    service = PostService(mock_repo)

    mock_redis = AsyncMock()
    # First call: Redis returns None (cache miss)
    mock_redis.get.return_value = None

    with patch("app.core.cache.get_redis_client", return_value=mock_redis):
        # 1st invocation -> Cache Miss -> DB repository called
        results_1 = await service.get_trending_posts(limit=10)
        assert mock_repo.get_trending.call_count == 1
        assert len(results_1) == 2
        mock_redis.get.assert_called_with("trending_posts:10")
        mock_redis.set.assert_called_once()

        # Simulate cached value returned on second call
        cached_json = mock_redis.set.call_args[1]["value"]
        mock_redis.get.return_value = cached_json

        # 2nd invocation -> Cache Hit -> DB repository NOT called again
        results_2 = await service.get_trending_posts(limit=10)
        assert mock_repo.get_trending.call_count == 1  # Still 1
        assert len(results_2) == 2
        assert results_2[0].title == "Trending Post 1"

@pytest.mark.asyncio
async def test_get_trending_posts_redis_none_fallback():
    mock_repo = MagicMock()
    mock_posts = [create_mock_post(1, "Trending Post 1", 100)]
    mock_repo.get_trending.return_value = mock_posts

    service = PostService(mock_repo)

    # When Redis client is None, it should gracefully call the repository without raising exception
    with patch("app.core.cache.get_redis_client", return_value=None):
        results = await service.get_trending_posts(limit=5)
        assert mock_repo.get_trending.call_count == 1
        assert len(results) == 1

def test_api_trending_endpoint():
    mock_posts = [
        create_mock_post(1, "API Trending Post 1", 150)
    ]
    with patch("app.core.dependency.PostRepository") as mock_repo_cls, \
         patch("app.core.cache.get_redis_client", return_value=None):
        instance = mock_repo_cls.return_value
        instance.get_trending.return_value = mock_posts

        client = TestClient(app)
        response = client.get("/api/v1/user_web/trending?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "API Trending Post 1"
