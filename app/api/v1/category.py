from fastapi import APIRouter
from typing import List
from app.core.dependency import get_category_service
from app.schemas.category import CategoryResponse, CategoryCreate

router = APIRouter()

@router.get("/category", response_model=List[CategoryResponse])
def get_categories():
    """
    Get all active categories.
    """
    service = get_category_service()
    return service.get_all_categories()

@router.post("/category", response_model=CategoryResponse)
def create_category(category_in: CategoryCreate):
    """
    Create a new category (internal or for admin use).
    """
    service = get_category_service()
    return service.create_category(category_in)
