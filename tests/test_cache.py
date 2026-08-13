import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.models.featured import FeaturedPost
from app.models.post import Post

client = TestClient(app)


class TestRedisCache(unittest.TestCase):
    def test_redis_none_fallback(self):
        with patch("app.core.cache.get_redis_client", return_value=None):
            with patch("app.services.featured.FeaturedPostService.get_all_featured") as mock_service:
                mock_service.return_value = [
                    FeaturedPost(id=1, title="Test 1", portrait_image="p1.jpg", image="i1.jpg")
                ]
                res = client.get("/api/v1/user_web/featured")
                self.assertEqual(res.status_code, 200)
                self.assertEqual(len(res.json()), 1)
                self.assertEqual(res.json()[0]["title"], "Test 1")
                self.assertEqual(mock_service.call_count, 1)

    def test_featured_route_caching(self):
        mock_redis = AsyncMock()
        cache_store = {}

        async def fake_get(key):
            return cache_store.get(key)

        async def fake_set(key, value, ex=None):
            cache_store[key] = value

        mock_redis.get.side_effect = fake_get
        mock_redis.set.side_effect = fake_set

        with patch("app.core.cache.get_redis_client", return_value=mock_redis):
            with patch("app.services.featured.FeaturedPostService.get_all_featured") as mock_service:
                mock_service.return_value = [
                    FeaturedPost(id=1, title="Featured 1", portrait_image="p1.jpg", image="i1.jpg")
                ]

                # Cache MISS
                res1 = client.get("/api/v1/user_web/featured")
                self.assertEqual(res1.status_code, 200)
                self.assertEqual(res1.json()[0]["title"], "Featured 1")
                self.assertEqual(mock_service.call_count, 1)
                self.assertIn("featured:get_featured_posts", cache_store)

                # Cache HIT
                res2 = client.get("/api/v1/user_web/featured")
                self.assertEqual(res2.status_code, 200)
                self.assertEqual(res2.json()[0]["title"], "Featured 1")
                self.assertEqual(mock_service.call_count, 1)

    def test_trending_route_caching(self):
        mock_redis = AsyncMock()
        cache_store = {}

        async def fake_get(key):
            return cache_store.get(key)

        async def fake_set(key, value, ex=None):
            cache_store[key] = value

        mock_redis.get.side_effect = fake_get
        mock_redis.set.side_effect = fake_set

        with patch("app.core.cache.get_redis_client", return_value=mock_redis):
            with patch("app.services.post.PostService.get_trending_posts") as mock_post_service:
                mock_post_service.return_value = [
                    Post(
                        id=10,
                        title="Trending Post 1",
                        title_translate="Trans 1",
                        description="Desc",
                        des="Des",
                        des_translate="Des Trans",
                        portrait_image="p.jpg",
                        image="i.jpg",
                        video=None,
                        link=None,
                        categories="Hiphop",
                        categories_id=1,
                        social_media="x",
                        views=500,
                        date="2026-08-13",
                        comment_count=2,
                    )
                ]

                # Cache MISS
                res1 = client.get("/api/v1/user_web/trending?limit=5")
                self.assertEqual(res1.status_code, 200)
                self.assertEqual(res1.json()[0]["title"], "Trending Post 1")
                self.assertEqual(mock_post_service.call_count, 1)
                self.assertIn("trending:5", cache_store)

                # Cache HIT
                res2 = client.get("/api/v1/user_web/trending?limit=5")
                self.assertEqual(res2.status_code, 200)
                self.assertEqual(res2.json()[0]["title"], "Trending Post 1")
                self.assertEqual(mock_post_service.call_count, 1)


if __name__ == "__main__":
    unittest.main()
