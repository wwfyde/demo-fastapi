import logging
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated, Literal

from fastapi import FastAPI, Body, Depends, UploadFile, File, Query
from pydantic import JsonValue
from redis.asyncio import Redis
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from uvicorn import run

from app import api2
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.dependencies import get_redis_cache, get_db
from app.models import Item


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("开机")
    logging.info("startup")
    yield
    print('关机')
    logging.info('shutdown')


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/info")
async def info():
    return {
        "project_name": settings.PROJECT_NAME,
        "demo": settings.PGUSER,
        "app_name": settings.app_name
    }


@app.post("/body")
async def body(
        item: Annotated[JsonValue, Body()],
        # item: Request,
):
    """
    允许传入任意类型的字符串
    :param item:
    :return:
    """
    print(item, type(item))
    item = {
        "a": 12,
        "b": 13,
    }
    return item


# @app.get('/self')
# async def self(request: Request):
#     client = TestClient(app)
#     response = client.get('/info')
#     return response.json()

@app.get('/cache')
async def cache_example(
        cache: Redis = Depends(get_redis_cache)
):
    await cache.set('my-key', 'value-flag')
    value = await cache.get('my-key')
    return value


@app.get('/pg_and_redis')
async def pg_and_redis(
        db: Session = Depends(get_db),
        cache: Redis = Depends(get_redis_cache)
):
    obj = db.get(Item, 1)
    return obj
    await cache.set('my-key', 'value-flag')
    value = await cache.get('my-key')
    return value


@app.post('/upload')
async def upload(
        file: Annotated[UploadFile, File(description='File')],
):
    return file.headers


class Color(str, Enum):
    red = "RED"
    green = "GREEN"
    blue = "BLUE"


@app.get('/enum')
async def enum_example(
        color: Annotated[Color, Query()] = Color.red
):
    return {
        'color': color.value
    }


@app.get('/literal')
async def literal_example(
        color: Literal['a', 'n', 'c'] = 'c'
):
    return {
        'color': color
    }


app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount('/outer', api2.app)

if __name__ == "__main__":
    run(app='main:app', reload=True, port=8199, workers=4)
