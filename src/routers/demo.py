import asyncio
import logging
import time
from enum import Enum
from typing import Annotated, Literal

from fastapi import APIRouter, Body, Depends, File, Query, UploadFile
from pydantic import JsonValue
from redis.asyncio import Redis
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse, StreamingResponse

from src.core.deps import get_db, get_redis_cache
from src.models import Item, LLM
from src.schemas.item import ItemCreate
from src import settings

router = APIRouter()
logger = logging.getLogger(__name__)


# next, instrument your database connector, http library etc. and add the logging handler
@router.get("/")
async def root():
    return RedirectResponse(url="/docs")


@router.get("/features", summary="重定向标识")
async def features_redirect():
    return RedirectResponse(url="/features/docs")


@router.post("/file/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@router.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@router.get("/info")
async def info():
    print(settings.project_name)
    print(settings.app_name)
    return {
        "project_name": settings.project_name,
        "app_name": settings.app_name,
        "settings_all": settings,
    }


@router.post("/body")
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


# @router.get('/self')
# async def self(request: Request):
#     client = TestClient(app)
#     response = client.get('/info')
#     return response.json()


@router.get("/cache")
async def cache_example(cache: Redis = Depends(get_redis_cache)):
    await cache.set("my-key", "value-flag")
    value = await cache.get("my-key")
    return value


@router.get("/pg_and_redis")
async def pg_and_redis(db: Session = Depends(get_db), cache: Redis = Depends(get_redis_cache)):
    obj = db.get(Item, 1)
    print(obj)
    stmt = select(Item).where(Item.id == 1)  # noqa
    db.execute(stmt)
    await cache.set("my-key", "value-flag")
    value = await cache.get("my-key")
    return value


@router.post("/upload")
async def upload(
    file: Annotated[UploadFile, File(description="File")],
):
    return file.headers


class Color(str, Enum):
    red = "RED"
    green = "GREEN"
    blue = "BLUE"


@router.get("/enum")
async def enum_example(color: Annotated[Color, Query()] = Color.red):
    return {"color": color.value}


@router.get("/literal")
async def literal_example(color: Literal["a", "n", "c"] = "c"):
    return {"color": color}


async def get_content():
    for i in range(100):
        yield str(i)
        await asyncio.sleep(0.1)


@router.get("/stream")
async def stream_example():
    return StreamingResponse(get_content(), media_type="text/event-stream")


def event_stream():
    count = 0
    while True:
        time.sleep(1)  # Simulate a delay for sending events
        count += 1
        yield f"data: Event {count}\n\n"


@router.get("/events")
async def events():
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/llm")
async def llm(db: Session = Depends(get_db)):
    llm_db = LLM(
        name="test2",
        # config=None
    )
    db.add(llm_db)
    db.commit()
    db.refresh(llm_db)
    return llm_db


@router.post("/items")
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
):
    item_db = Item()
    logger.info(str(item))
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(item_db, key, value)

    db.add(item_db)
    db.commit()
    logger.info(f"config type: {str(item.config)}, {item_db.config}")
    logger.info(f"config type: {type(item.config)}, {type(item_db.config)}")
    db.refresh(item_db)
    return item_db


@router.post("/items/v2")
async def create_item_v2(
    item: ItemCreate,
    db: Session = Depends(get_db),
):
    # 字段过滤
    print("表格字段:", Item.__table__.columns)
    new_item = {
        key: value for key, value in item.model_dump(exclude_unset=True).items() if key in Item.__table__.columns
    }
    print("过滤后的字段", new_item)
    item_db = Item(**new_item, description2="test")
    # item_db = Item(**item.model_dump(exclude_unset=True), description2='test')
    print("项目", item_db)
    print("项目", item.model_dump(exclude_unset=True))
    db.add(item_db)
    db.commit()
    logger.info(f"config type: {str(item.config)}, {item_db.config}")
    logger.info(f"config type: {type(item.config)}, {type(item_db.config)}")
    db.refresh(item_db)
    return item_db
