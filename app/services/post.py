import datetime
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate
from app.models.post import Post

class PostService:
    @staticmethod
    def get_post_by_id(db: Session, post_id: int, increment_view: bool = False) -> Optional[Post]:
        post = PostRepository.get_by_id(db, post_id)
        if post and increment_view:
            post = PostRepository.increment_views(db, post)
        return post

    @staticmethod
    def get_trending_posts(db: Session, limit: int = 10) -> List[Post]:
        return PostRepository.get_trending(db, limit)

    @staticmethod
    def get_posts_by_category(db: Session, category_id: int, limit: int = 10, offset: int = 0) -> List[Post]:
        return PostRepository.get_by_category_id(db, category_id, limit, offset)

    @staticmethod
    def get_posts_by_date(db: Session, date_str: str, limit: int = 10, offset: int = 0) -> List[Post]:
        return PostRepository.get_posts_by_date(db, date_str, limit, offset)

    @staticmethod
    def search_posts(db: Session, query: str, limit: int = 10, offset: int = 0) -> List[Post]:
        return PostRepository.search(db, query, limit, offset)

    @staticmethod
    def create_post(db: Session, post_in: PostCreate) -> Post:
        return PostRepository.create(db, post_in)

    @staticmethod
    def get_home_posts_grouped(db: Session, page: int = 1) -> dict:
        # Calculate dynamic dates relative to current local time
        today_dt = datetime.date.today()
        today_str = today_dt.strftime("%Y-%m-%d")
        yesterday_str = (today_dt - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        day_before_yesterday_str = (today_dt - datetime.timedelta(days=2)).strftime("%Y-%m-%d")

        # Basic pagination: limit posts per date bucket
        limit = 10
        offset = (page - 1) * limit

        # Retrieve posts for the computed dates
        today_posts = PostRepository.get_posts_by_date(db, today_str, limit, offset)
        yesterday_posts = PostRepository.get_posts_by_date(db, yesterday_str, limit, offset)
        dby_posts = PostRepository.get_posts_by_date(db, day_before_yesterday_str, limit, offset)

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
