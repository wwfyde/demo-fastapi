from fastapi import APIRouter

from . import data_join

router = APIRouter()

router.include_router(data_join.router, prefix="/data_join", tags=["Data Join"])
__all__ = ["router"]
