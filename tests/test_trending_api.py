import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from app.main import app
from app.models.post import Post
from app.core.dependency import get_post_service
from app.services.post import PostService

with patch("app.core.lifespan.open_connection"), patch("app.core.lifespan.close_connection"):
    client = TestClient(app)

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
        categories="HipHop",
        categories_id=1,
        social_media="@hiphop",
        views=2000,
        date="2026-08-10",
        comment_count=10
    )

def test_trending_api_endpoint(mock_post):
    mock_service = MagicMock(spec=PostService)
    async_get_trending = AsyncMock(return_value=[mock_post])
    mock_service.get_trending_posts = async_get_trending

    app.dependency_overrides[get_post_service] = lambda: mock_service

    try:
        response = client.get("/api/v1/user_web/trending?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["title"] == "Trending Post Title"
        mock_service.get_trending_posts.assert_called_once_with(5)
    finally:
        app.dependency_overrides.clear()
