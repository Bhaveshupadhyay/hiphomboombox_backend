from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate
from app.models.category import Category

class CategoryService:
    @staticmethod
    def get_all_categories(db: Session) -> List[Category]:
        return CategoryRepository.get_all(db)

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Optional[Category]:
        return CategoryRepository.get_by_id(db, category_id)

    @staticmethod
    def create_category(db: Session, category_in: CategoryCreate) -> Category:
        # Prevent duplicate categories by name
        existing = CategoryRepository.get_by_name(db, category_in.name)
        if existing:
            return existing
        return CategoryRepository.create(db, category_in)
