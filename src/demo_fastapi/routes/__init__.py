from fastapi import APIRouter

from . import cache_examples, demo, relationship, student_course, todo

router = APIRouter()

router.include_router(
    student_course.router, prefix="/relationship", tags=["Relationship"]
)
router.include_router(demo.router, prefix="", tags=["Demo"])
router.include_router(
    relationship.router, prefix="/relationship", tags=["Relationship"]
)
router.include_router(cache_examples.router, prefix="/cache", tags=["Cache"])

router.include_router(todo.router, prefix="/todo", tags=["Todo"])
__all__ = ["router"]
