import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, active_db_url, SessionLocal
from app.api.v1.router import api_router
from app.seeder import seed_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info(f"Initializing database tables using active connection: {active_db_url}")
    try:
        # Create tables in the target database (PostgreSQL or SQLite fallback)
        Base.metadata.create_all(bind=engine)
        
        # Seed DB with initial categories, featured carousel, and relative-dated posts
        db = SessionLocal()
        try:
            seed_db(db)
        except Exception as e:
            logger.error(f"Database seeding failed: {e}")
        finally:
            db.close()
    except Exception as e:
        logger.critical(f"Failed to initialize database tables: {e}")
    
    yield
    # Shutdown actions (if any needed in the future)

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
        "database": "PostgreSQL" if active_db_url.startswith("postgresql") else "SQLite",
        "docs_url": "/docs"
    }
