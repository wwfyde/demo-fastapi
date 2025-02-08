import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from uvicorn import run

from src.api.v1.api import api_router
from src.apps import features, pd_validate_serialize
from src.core.config import settings
from src.core.deps import get_logger
from src.routers import router

log = get_logger(name="fastapi")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("开机")
    logging.info("startup")

    yield
    print("关机")
    logging.info("shutdown")


root_path = os.getenv("ROOT_PATH", "") or settings.API_V1_STR

# logfire.configure()
# logfire.instrument_fastapi(app)
# logfire.info(f'{app.__doc__}')


def create_app(lifespan: callable = lifespan):
    """
    通过工厂函数创建app
    :return:
    """
    app = FastAPI(
        title=settings.project_name,
        root_path=root_path,
        # openapi_url="/openapi.json",
        lifespan=lifespan,
        openapi_tags=[],
        # openapi_prefix=root_path,
    )

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

    app.mount("/features", features.app)
    app.include_router((pd_validate_serialize.router), prefix="/pd_validate_serialize")
    return app


app = create_app()

app.include_router(router, prefix=root_path or settings.API_V1_STR)
app.include_router(api_router, prefix=root_path or settings.API_V1_STR)
app.include_router(features.router, prefix="/features", tags=["features", "default"])

# app.mount('/outer', api2.app)

if __name__ == "__main__":
    run(app="main:app", reload=True, port=8199, workers=4)
