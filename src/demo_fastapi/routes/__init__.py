from fastapi import APIRouter
from fastapi.params import Depends

from . import cache_examples, demo, depend_system, relationship, student_course, todo, auth
from ..core.deps import verify_token

router = APIRouter()

router.include_router(student_course.router, prefix="/relationship", tags=["Relationship"])
router.include_router(demo.router, prefix="", tags=["Demo"])
router.include_router(relationship.router, prefix="/relationship", tags=["Relationship"])
router.include_router(cache_examples.router, prefix="/cache", tags=["Cache"])

router.include_router(todo.router, prefix="/todo", tags=["Todo"], dependencies=[Depends(verify_token)])

router.include_router(depend_system.router, prefix="/depend_system", tags=["Depend System"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
__all__ = ["router"]
