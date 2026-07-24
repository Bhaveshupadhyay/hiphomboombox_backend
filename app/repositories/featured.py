from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.featured import FeaturedPost
from app.schemas.featured import FeaturedPostCreate

class FeaturedPostRepository:
    @staticmethod
    def get_all(db: Session) -> List[FeaturedPost]:
        return db.query(FeaturedPost).all()

    @staticmethod
    def get_by_id(db: Session, featured_id: int) -> Optional[FeaturedPost]:
        return db.query(FeaturedPost).filter(FeaturedPost.id == featured_id).first()

    @staticmethod
    def create(db: Session, featured_in: FeaturedPostCreate) -> FeaturedPost:
        db_featured = FeaturedPost(
            title=featured_in.title,
            portrait_image=featured_in.portrait_image,
            image=featured_in.image
        )
        db.add(db_featured)
        db.commit()
        db.refresh(db_featured)
        return db_featured
