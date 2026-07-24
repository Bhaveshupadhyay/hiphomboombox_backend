from contextlib import contextmanager
from typing import Generator

from app.repositories.category import CategoryRepository
from app.repositories.featured import FeaturedPostRepository
from app.repositories.post import PostRepository
from app.services.category import CategoryService
from app.services.featured import FeaturedPostService
from app.services.post import PostService
from app.core.client import get_postgres_client

# DB helper
@contextmanager
def get_db() -> Generator:
    session_local = get_postgres_client()
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Repositories (no parameter)
def get_category_repo() -> CategoryRepository:
    return CategoryRepository(get_db)

def get_featured_repo() -> FeaturedPostRepository:
    return FeaturedPostRepository(get_db)

def get_post_repo() -> PostRepository:
    return PostRepository(get_db)

# Services (no parameter)
def get_category_service() -> CategoryService:
    repo = get_category_repo()
    return CategoryService(repo)

def get_featured_service() -> FeaturedPostService:
    repo = get_featured_repo()
    return FeaturedPostService(repo)

def get_post_service() -> PostService:
    repo = get_post_repo()
    return PostService(repo)
