from fastapi import APIRouter
from app.api.v1.category import router as category_router
from app.api.v1.featured import router as featured_router
from app.api.v1.post import router as post_router

api_router = APIRouter()

# Register routes under the '/user_web' prefix to match frontend requirements
api_router.include_router(category_router, prefix="/user_web", tags=["Category"])
api_router.include_router(featured_router, prefix="/user_web", tags=["Featured"])
api_router.include_router(post_router, prefix="/user_web", tags=["Post"])
