from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.featured import FeaturedPostRepository
from app.schemas.featured import FeaturedPostCreate
from app.models.featured import FeaturedPost

class FeaturedPostService:
    @staticmethod
    def get_all_featured(db: Session) -> List[FeaturedPost]:
        return FeaturedPostRepository.get_all(db)

    @staticmethod
    def get_featured_by_id(db: Session, featured_id: int) -> Optional[FeaturedPost]:
        return FeaturedPostRepository.get_by_id(db, featured_id)

    @staticmethod
    def create_featured(db: Session, featured_in: FeaturedPostCreate) -> FeaturedPost:
        return FeaturedPostRepository.create(db, featured_in)
