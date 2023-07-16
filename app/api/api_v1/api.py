from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, demo, items

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(demo.router, prefix="/demo", tags=["demo"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
