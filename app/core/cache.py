import inspect
import json
import logging
from functools import wraps
from typing import Optional, Type, Any
from pydantic import TypeAdapter
from app.core.client import get_redis_client

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

            if key:
                key_parts = [str(func_args.get(k)) for k in key if k in func_args]
            else:
                key_parts = [str(v) for k, v in func_args.items() if k != "self"]

            cache_key = get_redis_key(namespace=namespace, key_parts=key_parts)

            redis_client = get_redis_client()
            if redis_client is not None:
                try:
                    cached_data = await redis_client.get(cache_key)
                    if cached_data:
                        logger.info(f"[CACHE HIT] Returning data for {cache_key}")
                        if return_type:
                            return TypeAdapter(return_type).validate_json(cached_data)
                        return json.loads(cached_data)
                except Exception as e:
                    logger.warning(f"Redis get error for key {cache_key}: {e}")

            logger.info(f"[CACHE MISS] Executing function for {cache_key}")

            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            if result is not None and redis_client is not None:
                try:
                    if return_type:
                        data_to_store = TypeAdapter(return_type).dump_json(result).decode('utf-8')
                    else:
                        try:
                            data_to_store = json.dumps(result)
                        except TypeError:
                            if isinstance(result, list):
                                data_to_store = json.dumps([item.__dict__ for item in result if hasattr(item, "__dict__")])
                            elif hasattr(result, "__dict__"):
                                data_to_store = json.dumps(result.__dict__)
                            else:
                                raise

                    await redis_client.set(key=cache_key, ex=redis_ttl, value=data_to_store)
                except Exception as e:
                    logger.warning(f"Redis set error for key {cache_key}: {e}")

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
    if redis_client is not None:
        try:
            cache_key = get_redis_key(namespace=namespace, key_parts=[key])
            await redis_client.set(key=cache_key, value=json.dumps(data), ex=redis_ttl)
        except Exception as e:
            logger.warning(f"Failed to insert redis data for key {key}: {e}")


def get_redis_key(namespace: str, key_parts: list[str]) -> str:
    return f"{namespace}:{':'.join(key_parts)}"

