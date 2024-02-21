from typing import Annotated, Any

from fastapi import FastAPI, Body
from httpx import Request
from pydantic import JsonValue
from starlette.responses import RedirectResponse
from uvicorn import run

from app import api2
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.session import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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


app.include_router(api_router, prefix=settings.API_V1_STR)

Base.metadata.create_all(bind=engine)

app.mount('/outer', api2.app)

if __name__ == "__main__":
    run(app='main:app', reload=True, port=8199, workers=4)
