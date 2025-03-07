from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Query

from .models import Student
from .schemas import StudentCreate, Validator

router = APIRouter()


@router.get("/items")
async def read_items(
        query: Annotated[Validator, Query()]
):
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.post("/items")
async def create_item(
        student_in: StudentCreate,
):
    student = Student()
    for key, value in student_in.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    return student
