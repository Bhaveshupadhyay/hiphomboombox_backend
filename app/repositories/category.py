from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.category import Category
from app.schemas.category import CategoryCreate

class CategoryRepository:
    @staticmethod
    def get_all(db: Session) -> List[Category]:
        return db.query(Category).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[Category]:
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    @staticmethod
    def create(db: Session, category_in: CategoryCreate) -> Category:
        db_category = Category(name=category_in.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
