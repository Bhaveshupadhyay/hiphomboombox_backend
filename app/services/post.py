import datetime
from typing import List, Optional, Dict
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostResponse
from app.models.post import Post
from app.core.cache import cached

class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_post_by_id(self, post_id: int, increment_view: bool = False) -> Optional[Post]:
        post = self.post_repo.get_by_id(post_id)
        if post and increment_view:
            post = self.post_repo.increment_views(post)
        return post

    @cached(
        namespace="trending_posts",
        key=["limit"],
        redis_ttl=3600,
        return_type=List[PostResponse]
    )
    async def get_trending_posts(self, limit: int = 10) -> List[PostResponse]:
        return self.post_repo.get_trending(limit)


    def get_posts_by_category(self, category_id: int, limit: int = 10, offset: int = 0) -> List[Post]:
        return self.post_repo.get_by_category_id(category_id, limit, offset)

    def get_posts_by_date(self, date_str: str, limit: int = 10, offset: int = 0) -> List[Post]:
        return self.post_repo.get_posts_by_date(date_str, limit, offset)

    def search_posts(self, query: str, limit: int = 10, offset: int = 0) -> List[Post]:
        return self.post_repo.search(query, limit, offset)

    def create_post(self, post_in: PostCreate) -> Post:
        return self.post_repo.create(post_in)

    def get_home_posts_grouped(self, page: int = 1) -> dict:
        # Calculate dynamic dates relative to current local time
        today_dt = datetime.date.today()
        today_str = today_dt.strftime("%Y-%m-%d")
        yesterday_str = (today_dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        day_before_yesterday_str = (today_dt - datetime.timedelta(days=2)).strftime("%Y-%m-%d")

        # Basic pagination: limit posts per date bucket
        limit = 10
        offset = (page - 1) * limit

        # Retrieve posts for the computed dates
        today_posts = self.post_repo.get_posts_by_date(today_str, limit, offset)
        yesterday_posts = self.post_repo.get_posts_by_date(yesterday_str, limit, offset)
        dby_posts = self.post_repo.get_posts_by_date(day_before_yesterday_str, limit, offset)

        return {
            "isSuccess": True,
            "today": today_str,
            "yesterday": yesterday_str,
            "day_before_yesterday": day_before_yesterday_str,
            "data": {
                "today": today_posts,
                "yesterday": yesterday_posts,
                "day_before_yesterday": dby_posts
            }
        }
