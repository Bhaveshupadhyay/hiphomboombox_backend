from typing import List, Optional
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate
from app.models.category import Category

class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    def get_all_categories(self) -> List[Category]:
        return self.category_repo.get_all()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.category_repo.get_by_id(category_id)

    def create_category(self, category_in: CategoryCreate) -> Category:
        existing = self.category_repo.get_by_name(category_in.name)
        if existing:
            return existing
        return self.category_repo.create(category_in)
