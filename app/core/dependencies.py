from typing import Generator

import redis.asyncio as redis
from celery import Celery
from sqlalchemy.orm import Session

from app.core.db import engine


# redis cache
async def get_redis_cache():
    r = redis.Redis(host='redis', port=6379, db=0)
    yield r
    await r.close()


# DB
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# celery
celery = Celery('tasks', broker='amqp://guest@rabbit//', backend='redis://redis:6379/0')
