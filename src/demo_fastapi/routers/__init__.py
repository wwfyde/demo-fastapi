from fastapi import APIRouter

from . import demo, relationship, student_course

router = APIRouter()

router.include_router(
    student_course.router, prefix="/relationship", tags=["Relationship"]
)
router.include_router(demo.router, prefix="", tags=["Demo"])
router.include_router(
    relationship.router, prefix="/relationship", tags=["Relationship"]
)
__all__ = ["router"]
