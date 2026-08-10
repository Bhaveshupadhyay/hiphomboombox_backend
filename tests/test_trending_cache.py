import json
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from typing import List

from app.models.category import Category
from app.models.post import Post
from app.schemas.post import PostResponse
from app.services.post import PostService
from app.repositories.post import PostRepository

@pytest.fixture
def mock_post():
    return Post(
        id=1,
        title="Trending Post Title",
        title_translate="Trending Post Title Translated",
        description="Trending post description",
        des="Trending post body content",
        des_translate="Trending post body content translated",
        portrait_image="https://example.com/portrait.jpg",
        image="https://example.com/image.jpg",
        video="https://example.com/video.mp4",
        link="https://example.com/post/1",
        categories="HipHop, Rap",
        categories_id=1,
        social_media="@hiphop",
        views=1500,
        date="2026-08-10",
        comment_count=42
    )

@pytest.mark.asyncio
async def test_get_trending_posts_cache_miss_and_hit(mock_post):
    mock_repo = MagicMock(spec=PostRepository)
    mock_repo.get_trending.return_value = [mock_post]
    service = PostService(mock_repo)

    mock_redis = AsyncMock()
    # On first call, Redis get returns None (cache miss)
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True

    with patch("app.core.cache.get_redis_client", return_value=mock_redis):
        # 1. First call: Cache Miss
        posts = await service.get_trending_posts(limit=10)
        assert len(posts) == 1
        assert posts[0].id == 1
        assert mock_repo.get_trending.call_count == 1
        mock_redis.get.assert_called_once_with("trending:10")
        mock_redis.set.assert_called_once()

        # Check key and payload set in Redis
        set_args = mock_redis.set.call_args[1]
        assert set_args["key"] == "trending:10"
        assert set_args["ex"] == 3600

        # Prepare cached payload for Cache Hit test
        cached_payload = set_args["value"]
        mock_redis.get.return_value = cached_payload
        mock_repo.get_trending.reset_mock()

        # 2. Second call: Cache Hit
        posts_cached = await service.get_trending_posts(limit=10)
        assert len(posts_cached) == 1
        assert posts_cached[0].id == 1
        # Repo should NOT be called again
        mock_repo.get_trending.assert_not_called()

@pytest.mark.asyncio
async def test_get_trending_posts_redis_disabled_fallback(mock_post):
    mock_repo = MagicMock(spec=PostRepository)
    mock_repo.get_trending.return_value = [mock_post]
    service = PostService(mock_repo)

    # When Redis client is None (credentials not configured)
    with patch("app.core.cache.get_redis_client", return_value=None):
        posts = await service.get_trending_posts(limit=10)
        assert len(posts) == 1
        assert posts[0].id == 1
        mock_repo.get_trending.assert_called_once_with(10)
