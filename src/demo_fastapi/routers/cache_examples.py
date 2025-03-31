import redis.asyncio as redis
from fastapi import APIRouter, Depends

from demo_fastapi.core.deps import get_redis_cache

router = APIRouter()


@router.get("/hello")
async def hello(cache: redis.Redis = Depends(get_redis_cache)):
    await cache.set("hello", "world")
    result = await cache.get("hello")
    return {"message": f"Hello, {result}!"}
