from fastapi import FastAPI
from uvicorn import run

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.db.session import engine, Base

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    run(app='main:app', reload=True, port=8199, workers=4)
