import inspect
import json
import logging
from functools import wraps
from typing import Optional, Type, Any
from app.core.client import get_redis_client

from pydantic import TypeAdapter

logger = logging.getLogger(__name__)

def cached(
    namespace: str = "default",
    key: Optional[list[str]] = None,
    redis_ttl: int = 3600,
    return_type: Optional[Type[Any]] = None,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            func_args = bound_args.arguments

            if not key:
                cache_key = get_redis_key(namespace=namespace, key_parts=[])
            else:
                key_parts = [str(func_args.get(k)) for k in key if k in func_args]
                cache_key = get_redis_key(namespace=namespace, key_parts=key_parts)

            redis_client = get_redis_client()
            if redis_client is None:
                if inspect.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                return func(*args, **kwargs)

            try:
                cached_data = await redis_client.get(cache_key)
                if cached_data:
                    logger.info(f"[CACHE HIT] Returning data for {cache_key}")
                    if return_type:
                        return TypeAdapter(return_type).validate_json(cached_data)
                    return json.loads(cached_data)
            except Exception as e:
                logger.warning(f"[CACHE ERROR] Failed to fetch cache for key {cache_key}: {e}")

            logger.info(f"[CACHE MISS] Executing function for {cache_key}")

            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if result is not None:
                try:
                    if return_type:
                        data_to_store = TypeAdapter(return_type).dump_json(result).decode('utf-8')
                    else:
                        data_to_store = json.dumps(result)

                    await redis_client.set(key=cache_key, ex=redis_ttl, value=data_to_store)
                except Exception as e:
                    logger.warning(f"[CACHE ERROR] Failed to write cache for key {cache_key}: {e}")

            return result
        return wrapper
    return decorator


async def insert_redis_data(
    key: str,
    namespace: str = "default",
    redis_ttl: int = 3600,
    data: Any = None,
):
    redis_client = get_redis_client()
    if redis_client:
        await redis_client.set(
            key=get_redis_key(namespace=namespace, key_parts=[key]),
            value=json.dumps(data),
            ex=redis_ttl,
        )


def get_redis_key(namespace: str, key_parts: list[str]) -> str:
    if key_parts:
        return f"{namespace}:{':'.join(key_parts)}"
    return namespace

