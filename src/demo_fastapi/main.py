import asyncio
import logging
import os
import threading
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, Request
from fastapi.applications import AppType
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, RedirectResponse
from uvicorn import run

from demo_fastapi.api.v1.api import api_router
from demo_fastapi.apps import features, pd_validate_serialize
from demo_fastapi.core.config import settings
from demo_fastapi.core.deps import logger, get_var_with_params
from demo_fastapi.routes import router


def interval_task():
    print("interval_task initial")
    while True:
        time.sleep(2)
        # print("interval_task")


async def listen_service():
    print("listen_service initial")
    while True:
        await asyncio.sleep(5)
        # print("listen_service")


@asynccontextmanager
async def lifespan(app: AppType):
    print("开机")
    logging.info("startup")
    # 启动一个线程
    thread = threading.Thread(target=interval_task, daemon=True)
    thread.start()

    # 异步任务
    app.state.listen_task = asyncio.create_task(listen_service())

    # 全局共享状态
    app.state.demo = 12

    # 全局请求计数
    app.state.request_count = 0

    yield
    print("关机")
    logging.info("shutdown")
    app.state.listen_task.cancel()


root_path = os.getenv("ROOT_PATH", "") or settings.api_prefix


async def verify_custom_token(token: str = Header(None)):
    if not token or token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token


async def log_requests():
    logging.info("Request received")
    return "logged"


def create_app(lifespan: callable = lifespan):
    """
    通过工厂函数创建app
    :return:
    """
    import sys

    print(sys.path)
    logger.info(sys.path)

    app = FastAPI(
        title=settings.project_name,
        # root_path=root_path,  # 这种写法不对
        # openapi_url="/openapi.json",
        lifespan=lifespan,
        openapi_tags=[],
        openapi_prefix="",
        # dependencies=[Depends(log_requests)],  # Depends(verify_custom_token),
    )

    # @app.middleware("http")
    # async def add_process_time_header(request: Request, call_next):
    #     start_time = time.perf_counter()
    #     response = await call_next(request)
    #     process_time = time.perf_counter() - start_time
    #     response.headers["X-Process-Time"] = str(process_time)
    #     log.debug(f"Process time: {process_time * 1000}ms")
    #     return response

    app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.CORS_ORIGINS,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_middleware(HeaderMiddleware)

    # register exception_handler
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={"code": 400, "message": f"request params error: {exc.body}"},
        )

    # 解决未开启魔法时无法访问问题
    @app.get("/docs2")
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title="API Docs",
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get("/")
    async def root():
        return RedirectResponse("/docs")

    @app.get("/hello")
    @app.get("/demo")
    async def hello(request: Request):
        s: str = "世界"
        from package2 import hello

        print(hello())
        from demo import demo

        print(request.app.state.demo)

        demo()
        return {"message": f"Hello, {s}!", "data": f"hello, {s}!"}

    @app.get("/deps_with_param")
    async def deps_with_param(param: str = Depends(get_var_with_params("你好"))):
        return {"message": f"Hello, {param}!"}

    @app.get("/deps_with_param2")
    async def deps_with_param2(param: str = Depends(get_var_with_params("世界"))):
        return {"message": f"Hello, {param}!"}

    app.mount("/features", features.app)
    app.include_router(pd_validate_serialize.router, prefix="/pd_validate_serialize")
    app.include_router(router, prefix=root_path or settings.api_prefix)
    app.include_router(api_router, prefix=root_path or settings.api_prefix)
    app.include_router(features.router, prefix="/features", tags=["features", "default"])
    # registering logfire
    # import logfire
    #
    # logfire.configure()
    # logfire.instrument_fastapi(app)
    # logfire.info(f"{app.__doc__}")

    if settings.trace and settings.trace.api_analytics:
        from api_analytics.fastapi import Analytics

        app.add_middleware(Analytics, api_key=settings.trace.api_analytics.api_key)
    # registering api-analytics
    return app


app = create_app()
print(f"首页执行{app}")


# app.mount('/outer', api2.app)

if __name__ == "__main__":
    run(app="main:app", reload=True, port=8199, workers=4)
