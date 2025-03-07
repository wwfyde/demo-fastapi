import asyncio
import logging
import time
from logging.handlers import RotatingFileHandler
from typing import Annotated, AsyncGenerator, Generator

import redis as redis_sync
import redis.asyncio as redis
from celery import Celery
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session

from demo_fastapi.core.config import settings
from demo_fastapi.core.db import async_engine, engine
from demo_fastapi.core.decorators import time_decorator


# redis cache
async def get_redis_cache() -> AsyncGenerator[redis.Redis, None]:
    """
    https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html

    :return:
    """
    pool = redis.ConnectionPool.from_url(
        settings.redis_dsn,
        decode_responses=True,
        protocol=3,
        health_check_interval=2,
        retry_on_timeout=True,
        max_connections=10,
    )
    async with redis.Redis.from_pool(pool) as r:
        # async with redis.Redis(connection_pool=pool) as r:  # deprecated
        yield r
        print("Redis 客户端关闭")
        await r.aclose()


def get_redis_cache_sync() -> Generator[redis_sync.Redis, None, None]:
    """
    :return:
    """
    pool = redis_sync.ConnectionPool.from_url(
        settings.redis_dsn, decode_responses=True, protocol=3, health_check_interval=2
    )
    with redis_sync.Redis(connection_pool=pool) as r:
        yield r


# DB
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


DBSession = Annotated[Session, Depends(get_db)]

async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db_async() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


DBSessionAsync = Annotated[AsyncSession, Depends(get_db_async)]


async def get_async_redis_cache() -> AsyncGenerator[redis.Redis, None]:
    pool = redis.ConnectionPool.from_url(
        settings.redis_dsn, decode_responses=True, protocol=3
    )
    r = redis.Redis(connection_pool=pool, decode_responses=True, protocol=3)
    async with r:
        print(await r.get("a"))
        yield r


async def get_async_redis_cache2() -> AsyncGenerator[redis.Redis, None]:
    pool = redis.ConnectionPool.from_url(
        settings.redis_dsn, decode_responses=True, protocol=3
    )
    r = redis.Redis(connection_pool=pool, decode_responses=True, protocol=3)
    try:
        yield r
    finally:
        await r.close()


def get_logger(name: str = __name__, write_to_file: bool = False) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 设置日志级别
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s [in %(pathname)s:%(lineno)d]"
    )

    if write_to_file is True:
        log_file = settings.log_file_path.joinpath(f"{name}.log")
        handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)
        handler.setLevel(logging.WARNING)  # 设置处理器的日志级别
        handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # 创建标准输出处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # 设置处理器的日志级别
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


class RateLimiter:
    """
    example:
        rate_limiter = RateLimiter(capacity=1, rate=0.2, refill_time=0.1)
        for _ in range(10):
            await rate_limiter.wait()
            # do something
    """

    def __init__(self, capacity: int, rate: float, refill_time: float = 0.1):
        # 设置桶容量
        self.capacity = capacity
        self.tokens = capacity  # 持有tokens

        # 速率限制
        self.rate = rate  # 单位时间能够添加的令牌数
        self.refill_time = refill_time  # 检查速率
        self.last_refill_time = time.time()  # 最后一次检查时间

    def add_tokens(self):
        now = time.time()
        elapsed_time = now - self.last_refill_time
        # 超过一定时间后, 添加一个令牌
        self.tokens += elapsed_time * self.rate
        self.last_refill_time = now

        # 向令牌中添加令牌, 但不能操过容量
        self.tokens = min(self.capacity, self.tokens)
        # 重置检查时间

    @time_decorator
    async def wait(self, tokens: int = 1):
        while True:
            self.add_tokens()
            # 如果桶中有足够的令牌, 则减去令牌
            if self.tokens >= tokens:
                self.tokens -= tokens
                break
            await asyncio.sleep(self.refill_time)


# celery
celery = Celery("tasks", broker="amqp://guest@rabbit//", backend="redis://redis:6379/0")


async def main():
    async with await get_redis_cache().__anext__() as r:
        print(await r.get("a"))


if __name__ == "__main__":
    asyncio.run(main())
