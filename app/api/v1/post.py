from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.core.dependency import get_post_service
from app.schemas.post import PostResponse, PostCreate, PostsResponse
from app.core.cache import cached

router = APIRouter()

@router.get("/posts", response_model=PostsResponse)
def get_posts(page: int = Query(1, ge=1)):
    """
    Get homepage posts grouped by today, yesterday, and day before yesterday.
    """
    service = get_post_service()
    return service.get_home_posts_grouped(page)

@router.get("/trending", response_model=List[PostResponse])
@cached(namespace="trending", key=["limit"], redis_ttl=3600, return_type=List[PostResponse])
async def get_trending_posts(limit: int = Query(10, ge=1)):
    """
    Get trending posts sorted by view count descending.
    """
    service = get_post_service()
    return service.get_trending_posts(limit)

@router.get("/post/{post_id}", response_model=PostResponse)
def get_post_by_id(post_id: int):
    """
    Get a single post's details by ID and automatically increment its view count.
    """
    service = get_post_service()
    post = service.get_post_by_id(post_id, increment_view=True)
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found")
    return post

@router.get("/category_post/{category_id}", response_model=List[PostResponse])
def get_posts_by_category(
    category_id: int,
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1)
):
    """
    Get posts belonging to a specific category.
    """
    offset = (page - 1) * limit
    service = get_post_service()
    return service.get_posts_by_category(category_id, limit, offset)

@router.get("/post_date/{date_str}", response_model=List[PostResponse])
def get_posts_by_date(
    date_str: str,
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1)
):
    """
    Get posts by a specific date string (e.g. YYYY-MM-DD).
    """
    offset = (page - 1) * limit
    service = get_post_service()
    return service.get_posts_by_date(date_str, limit, offset)

@router.get("/search", response_model=List[PostResponse])
def search_posts(
    q: Optional[str] = Query(None),
    query: Optional[str] = Query(None),
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1)
):
    """
    Search posts by query string matching title, description, body text, or category names.
    Supports either 'q' or 'query' as parameter.
    """
    search_term = q or query
    if not search_term:
        raise HTTPException(status_code=400, detail="Search query parameter 'q' or 'query' is required")
    offset = (page - 1) * limit
    service = get_post_service()
    return service.search_posts(search_term, limit, offset)

@router.post("/post", response_model=PostResponse)
def create_post(post_in: PostCreate):
    """
    Create a new post.
    """
    service = get_post_service()
    return service.create_post(post_in)
