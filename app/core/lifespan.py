import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.client import open_connection, close_connection

logger = logging.getLogger("lifespan")

@asynccontextmanager
async def lifespan(app: FastAPI):
    open_connection()
    yield
    await close_connection()
