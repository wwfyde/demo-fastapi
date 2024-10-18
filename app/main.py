import asyncio
import logging
import time
from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated, Literal

from fastapi import Body, Depends, FastAPI, File, Query, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from pydantic import JsonValue
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, RedirectResponse, StreamingResponse
from uvicorn import run

from app.api.v1.api import api_router
from app.apps import features, pd_validate_serialize
from app.core.config import settings
from app.core.dependencies import get_db, get_logger, get_redis_cache
from app.models import Item, LLM
from app.schemas.item import ItemCreate

log = get_logger(name="fastapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("开机")
    logging.info("startup")

    yield
    print("关机")
    logging.info("shutdown")


def create_app(lifespan: callable = lifespan):
    """
    通过工厂函数创建app
    :return:
    """
    app = FastAPI(
        title=settings.project_name,
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        lifespan=lifespan,
        openapi_tags=[],
    )
    app.mount("/features", features.app)
    app.include_router((pd_validate_serialize.router), prefix="/pd_validate_serialize")
    return app


app = create_app()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    # log.debug(f"Process time: {process_time * 1000}ms")
    return response


# register exception_handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": f"request params error: {exc.body}"},
    )


# logfire.configure()
# logfire.instrument_fastapi(app)
# logfire.info(f'{app.__doc__}')


# next, instrument your database connector, http library etc. and add the logging handler
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/features", summary="重定向标识")
async def features_redirect():
    return RedirectResponse(url="/features/docs")


@app.post("/file/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/info")
async def info():
    return {
        "project_name": settings.project_name,
        "app_name": settings.app_name,
        "settings": settings.nested.book.name,
        "demo": settings.nested.demo,
        "settings_all": settings,
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


@app.get("/cache")
async def cache_example(cache: Redis = Depends(get_redis_cache)):
    await cache.set("my-key", "value-flag")
    value = await cache.get("my-key")
    return value


@app.get("/pg_and_redis")
async def pg_and_redis(db: Session = Depends(get_db), cache: Redis = Depends(get_redis_cache)):
    obj = db.get(Item, 1)
    print(obj)
    stmt = select(Item).where(Item.id == 1)  # noqa
    db.execute(stmt)
    await cache.set("my-key", "value-flag")
    value = await cache.get("my-key")
    return value


@app.post("/upload")
async def upload(
    file: Annotated[UploadFile, File(description="File")],
):
    return file.headers


class Color(str, Enum):
    red = "RED"
    green = "GREEN"
    blue = "BLUE"


@app.get("/enum")
async def enum_example(color: Annotated[Color, Query()] = Color.red):
    return {"color": color.value}


@app.get("/literal")
async def literal_example(color: Literal["a", "n", "c"] = "c"):
    return {"color": color}


async def get_content():
    for i in range(100):
        yield str(i)
        await asyncio.sleep(0.1)


@app.get("/stream")
async def stream_example():
    return StreamingResponse(get_content(), media_type="text/event-stream")


def event_stream():
    count = 0
    while True:
        time.sleep(1)  # Simulate a delay for sending events
        count += 1
        yield f"data: Event {count}\n\n"


@app.get("/events")
async def events():
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/llm")
async def llm(db: Session = Depends(get_db)):
    llm_db = LLM(
        name="test2",
        # config=None
    )
    db.add(llm_db)
    db.commit()
    db.refresh(llm_db)
    return llm_db


@app.post("/items")
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
):
    item_db = Item()
    log.info(str(item))
    for key, value in item.model_dump(exclude_unset=True).items():
        setattr(item_db, key, value)

    db.add(item_db)
    db.commit()
    log.info(f"config type: {str(item.config)}, {item_db.config}")
    log.info(f"config type: {type(item.config)}, {type(item_db.config)}")
    db.refresh(item_db)
    return item_db


@app.post("/items/v2")
async def create_item(
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
    log.info(f"config type: {str(item.config)}, {item_db.config}")
    log.info(f"config type: {type(item.config)}, {type(item_db.config)}")
    db.refresh(item_db)
    return item_db


app.include_router(api_router, prefix=settings.api_v1_str)

# app.mount('/outer', api2.app)

if __name__ == "__main__":
    run(app="main:app", reload=True, port=8199, workers=4)
