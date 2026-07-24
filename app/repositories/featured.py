from typing import List, Optional
from app.models.featured import FeaturedPost
from app.schemas.featured import FeaturedPostCreate

class FeaturedPostRepository:
    def __init__(self, get_db):
        self.get_db = get_db

    def get_all(self) -> List[FeaturedPost]:
        with self.get_db() as db:
            return db.query(FeaturedPost).all()

    def get_by_id(self, featured_id: int) -> Optional[FeaturedPost]:
        with self.get_db() as db:
            return db.query(FeaturedPost).filter(FeaturedPost.id == featured_id).first()

    def create(self, featured_in: FeaturedPostCreate) -> FeaturedPost:
        db_featured = FeaturedPost(
            title=featured_in.title,
            portrait_image=featured_in.portrait_image,
            image=featured_in.image
        )
        with self.get_db() as db:
            db.add(db_featured)
            db.commit()
            db.refresh(db_featured)
            return db_featured
