import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

logger = logging.getLogger("database")
logging.basicConfig(level=logging.INFO)

# Base class for DB models
Base = declarative_base()

def get_engine_and_url():
    # If the database URL points to Postgres, test if Postgres is reachable
    if DATABASE_URL.startswith("postgresql"):
        try:
            # Create an engine with a short timeout to check if postgres is online
            temp_engine = create_engine(
                DATABASE_URL,
                connect_args={"connect_timeout": 2}
            )
            # Try to connect
            with temp_engine.connect() as conn:
                logger.info("Successfully connected to PostgreSQL database!")
            return temp_engine, DATABASE_URL
        except Exception as e:
            logger.warning(
                f"Failed to connect to PostgreSQL at {DATABASE_URL} (error: {e}). "
                "Falling back to local SQLite database: sqlite:///./hiphopboombox.db"
            )
            sqlite_url = "sqlite:///./hiphopboombox.db"
            # SQLite engine needs check_same_thread: False
            engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
            return engine, sqlite_url
    else:
        # SQLite
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        return engine, DATABASE_URL

engine, active_db_url = get_engine_and_url()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
