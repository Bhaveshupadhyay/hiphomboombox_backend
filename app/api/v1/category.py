from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.category import CategoryResponse, CategoryCreate
from app.services.category import CategoryService

router = APIRouter()

@router.get("/category", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Get all active categories.
    """
    return CategoryService.get_all_categories(db)

@router.post("/category", response_model=CategoryResponse)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category (internal or for admin use).
    """
    return CategoryService.create_category(db, category_in)
