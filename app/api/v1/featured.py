from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.featured import FeaturedPostResponse, FeaturedPostCreate
from app.services.featured import FeaturedPostService

router = APIRouter()

@router.get("/featured", response_model=List[FeaturedPostResponse])
def get_featured_posts(db: Session = Depends(get_db)):
    """
    Get all featured posts for the desktop and mobile homepage carousel.
    """
    return FeaturedPostService.get_all_featured(db)

@router.post("/featured", response_model=FeaturedPostResponse)
def create_featured_post(featured_in: FeaturedPostCreate, db: Session = Depends(get_db)):
    """
    Create a new featured post (internal or for admin use).
    """
    return FeaturedPostService.create_featured(db, featured_in)
