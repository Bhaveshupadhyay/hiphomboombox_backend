from typing import List, Optional
from app.repositories.featured import FeaturedPostRepository
from app.schemas.featured import FeaturedPostCreate
from app.models.featured import FeaturedPost

class FeaturedPostService:
    def __init__(self, featured_repo: FeaturedPostRepository):
        self.featured_repo = featured_repo

    def get_all_featured(self) -> List[FeaturedPost]:
        return self.featured_repo.get_all()

    def get_featured_by_id(self, featured_id: int) -> Optional[FeaturedPost]:
        return self.featured_repo.get_by_id(featured_id)

    def create_featured(self, featured_in: FeaturedPostCreate) -> FeaturedPost:
        return self.featured_repo.create(featured_in)
