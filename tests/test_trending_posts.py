import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from typing import List
from app.models.category import Category
from app.models.post import Post
from app.schemas.post import PostResponse
from app.services.post import PostService
from app.repositories.post import PostRepository

@pytest.fixture
def mock_post_repo():
    repo = MagicMock(spec=PostRepository)
    sample_posts = [
        Post(
            id=1,
            title="Post 1",
            title_translate="Post 1 Trans",
            description="Desc 1",
            des="Des 1",
            des_translate="Des Trans 1",
            portrait_image="p1.jpg",
            image="img1.jpg",
            video=None,
            link=None,
            categories="News",
            categories_id=1,
            social_media="twitter",
            views=150,
            date="2026-08-10",
            comment_count=10,
        ),
        Post(
            id=2,
            title="Post 2",
            title_translate="Post 2 Trans",
            description="Desc 2",
            des="Des 2",
            des_translate="Des Trans 2",
            portrait_image="p2.jpg",
            image="img2.jpg",
            video=None,
            link=None,
            categories="Music",
            categories_id=2,
            social_media="instagram",
            views=100,
            date="2026-08-10",
            comment_count=5,
        ),
    ]
    repo.get_trending.return_value = sample_posts
    return repo

@pytest.mark.asyncio
async def test_get_trending_posts_cache_miss_and_hit(mock_post_repo):
    service = PostService(mock_post_repo)

    mock_redis = AsyncMock()
    mock_redis.get.return_value = None  # Cache miss initially
    mock_redis.set.return_value = True

    with patch("app.core.cache.get_redis_client", return_value=mock_redis):
        # 1. First call - Cache Miss
        result1 = await service.get_trending_posts(limit=2)
        assert len(result1) == 2
        assert result1[0].id == 1
        assert result1[1].id == 2
        mock_post_repo.get_trending.assert_called_once_with(2)
        mock_redis.get.assert_called_once_with("posts:trending:2")
        mock_redis.set.assert_called_once()

        # 2. Mock Redis returning cached JSON for second call
        cached_json = mock_redis.set.call_args[1]["value"]
        mock_redis.get.return_value = cached_json

        mock_post_repo.get_trending.reset_mock()

        # Second call - Cache Hit
        result2 = await service.get_trending_posts(limit=2)
        assert len(result2) == 2
        assert result2[0].id == 1
        assert result2[1].id == 2
        mock_post_repo.get_trending.assert_not_called()

@pytest.mark.asyncio
async def test_get_trending_posts_no_redis(mock_post_repo):
    service = PostService(mock_post_repo)

    with patch("app.core.cache.get_redis_client", return_value=None):
        result = await service.get_trending_posts(limit=2)
        assert len(result) == 2
        assert result[0].id == 1
        mock_post_repo.get_trending.assert_called_once_with(2)
