from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.post import Post
from app.schemas.post import PostCreate

class PostRepository:
    @staticmethod
    def get_by_id(db: Session, post_id: int) -> Optional[Post]:
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def get_posts_by_date(db: Session, date_str: str, limit: int = 10, offset: int = 0) -> List[Post]:
        return db.query(Post).filter(Post.date == date_str).order_by(Post.id.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_trending(db: Session, limit: int = 10) -> List[Post]:
        return db.query(Post).order_by(Post.views.desc()).limit(limit).all()

    @staticmethod
    def get_by_category_id(db: Session, category_id: int, limit: int = 10, offset: int = 0) -> List[Post]:
        return db.query(Post).filter(Post.categories_id == category_id).order_by(Post.id.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def search(db: Session, search_query: str, limit: int = 10, offset: int = 0) -> List[Post]:
        search_filter = f"%{search_query}%"
        return db.query(Post).filter(
            or_(
                Post.title.ilike(search_filter),
                Post.title_translate.ilike(search_filter),
                Post.description.ilike(search_filter),
                Post.des.ilike(search_filter),
                Post.des_translate.ilike(search_filter),
                Post.categories.ilike(search_filter)
            )
        ).order_by(Post.id.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def create(db: Session, post_in: PostCreate) -> Post:
        db_post = Post(
            title=post_in.title,
            title_translate=post_in.title_translate,
            description=post_in.description,
            des=post_in.des,
            des_translate=post_in.des_translate,
            portrait_image=post_in.portrait_image,
            image=post_in.image,
            video=post_in.video,
            link=post_in.link,
            categories=post_in.categories,
            categories_id=post_in.categories_id,
            social_media=post_in.social_media,
            views=post_in.views,
            date=post_in.date,
            comment_count=post_in.comment_count
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    def increment_views(db: Session, post: Post) -> Post:
        post.views += 1
        db.commit()
        db.refresh(post)
        return post
