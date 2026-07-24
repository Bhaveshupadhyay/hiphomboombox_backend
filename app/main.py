import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.lifespan import lifespan

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")

app = FastAPI(
    title="HipHopBoomBox API",
    description="FastAPI Backend for the HipHopBoomBox User Web Application",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the versioned API router under '/api/v1'
app.include_router(api_router, prefix="/api/v1")

@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    """
    Root status check endpoint.
    """
    return {
        "status": "online",
        "app": "HipHopBoomBox Backend API",
        "docs_url": "/docs"
    }
