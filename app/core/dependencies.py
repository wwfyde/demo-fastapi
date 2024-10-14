import asyncio
import logging
import redis as redis_sync
import redis.asyncio as redis
from celery import Celery
from logging.handlers import RotatingFileHandler
from sqlalchemy.orm import Session
from typing import Generator, AsyncGenerator

from app import settings
from app.core.db import engine


# redis cache
async def get_redis_cache() -> Generator[redis.Redis, None, None]:
    pool = redis.ConnectionPool.from_url(settings.redis_dsn, decode_responses=True, protocol=3)
    async with redis.Redis(connection_pool=pool, decode_responses=True, protocol=3) as r:
        yield r


def get_redis_cache_sync() -> Generator[redis_sync.Redis, None, None]:
    pool = redis_sync.ConnectionPool(decode_responses=True, protocol=3)
    with redis_sync.Redis(connection_pool=pool, host='redis', port=6379, db=0, decode_responses=True, protocol=3) as r:
        yield r


# DB
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


async def get_async_redis_cache() -> AsyncGenerator[redis.Redis, None]:
    pool = redis.ConnectionPool.from_url(settings.redis_dsn, decode_responses=True, protocol=3)
    r = redis.Redis(connection_pool=pool, decode_responses=True, protocol=3)
    async with r:
        print(await r.get("a"))
        yield r


async def get_async_redis_cache2() -> AsyncGenerator[redis.Redis, None]:
    pool = redis.ConnectionPool.from_url(settings.redis_dsn, decode_responses=True, protocol=3)
    r = redis.Redis(connection_pool=pool, decode_responses=True, protocol=3)
    try:
        yield r
    finally:
        await r.close()


def get_logger(name: str = __name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置日志级别

    log_file = settings.log_file_path.joinpath(f"{name}.log")
    handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
    handler.setLevel(logging.WARNING)  # 设置处理器的日志级别
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s [in %(pathname)s:%(lineno)d]")
    handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # 创建标准输出处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # 设置处理器的日志级别
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


# celery
celery = Celery('tasks', broker='amqp://guest@rabbit//', backend='redis://redis:6379/0')


async def main():
    async with await get_redis_cache().__anext__() as r:
        print(await r.get("a"))


if __name__ == '__main__':
    asyncio.run(main())
