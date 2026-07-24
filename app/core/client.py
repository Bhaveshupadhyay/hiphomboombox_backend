import logging
import urllib.parse
from contextlib import contextmanager
from upstash_redis.asyncio import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

logger = logging.getLogger("database")
logging.basicConfig(level=logging.INFO)

Base = declarative_base()

_redis_client: Redis | None = None
_postgres_client: sessionmaker | None = None

def get_postgres_client() -> sessionmaker:
    global _postgres_client
    if _postgres_client is None:
        raw_password = settings.POSTGRES_PASSWORD
        encoded_password = urllib.parse.quote_plus(raw_password)

        DB_HOST = settings.POSTGRES_HOST

        SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{encoded_password}@{DB_HOST}:5432/postgres?sslmode=require"

        engine = create_engine(SQLALCHEMY_DATABASE_URL)

        _postgres_client = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _postgres_client

def get_redis_client() -> Redis | None:
    global _redis_client
    if _redis_client is None:
        url = settings.UPSTASH_REDIS_REST_URL
        token = settings.UPSTASH_REDIS_REST_TOKEN
        if url and token:
            _redis_client = Redis(url=url, token=token)
            logger.info("Successfully connected to Upstash Redis client!")
        else:
            logger.warning("Upstash Redis credentials (UPSTASH_REDIS_REST_URL, UPSTASH_REDIS_REST_TOKEN) not set. Skipping Redis initialization.")
    return _redis_client

def open_connection() -> None:
    get_redis_client()

async def close_redis_client() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None

def close_postgres_client() -> None:
    pass

async def close_connection():
    await close_redis_client()
    close_postgres_client()