from fastapi import APIRouter
from typing import List
from app.core.dependency import get_featured_service
from app.schemas.featured import FeaturedPostResponse, FeaturedPostCreate
from app.core.cache import cached, delete_redis_key

router = APIRouter()

@router.get("/featured", response_model=List[FeaturedPostResponse])
@cached(namespace="featured", key=[], redis_ttl=3600, return_type=List[FeaturedPostResponse])
async def get_featured_posts():
    """
    Get all featured posts for the desktop and mobile homepage carousel.
    """
    service = get_featured_service()
    return service.get_all_featured()

@router.post("/featured", response_model=FeaturedPostResponse)
async def create_featured_post(featured_in: FeaturedPostCreate):
    """
    Create a new featured post (internal or for admin use).
    """
    service = get_featured_service()
    result = service.create_featured(featured_in)
    await delete_redis_key("get_featured_posts", namespace="featured")
    return result

