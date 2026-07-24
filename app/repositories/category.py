from typing import List, Optional
from app.models.category import Category
from app.schemas.category import CategoryCreate

class CategoryRepository:
    def __init__(self, get_db):
        self.get_db = get_db

    def get_all(self) -> List[Category]:
        with self.get_db() as db:
            return db.query(Category).all()

    def get_by_id(self, category_id: int) -> Optional[Category]:
        with self.get_db() as db:
            return db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, name: str) -> Optional[Category]:
        with self.get_db() as db:
            return db.query(Category).filter(Category.name == name).first()

    def create(self, category_in: CategoryCreate) -> Category:
        db_category = Category(name=category_in.name)
        with self.get_db() as db:
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            return db_category
