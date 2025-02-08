from fastapi import APIRouter

from . import data_join, demo

router = APIRouter()

router.include_router(data_join.router, prefix="/data_join", tags=["Data Join"])
router.include_router(demo.router, prefix="", tags=["Demo"])
__all__ = ["router"]
