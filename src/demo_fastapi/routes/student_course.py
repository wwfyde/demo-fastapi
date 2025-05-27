from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from demo_fastapi.core.deps import get_db_async
from demo_fastapi.models import Course, Student
from demo_fastapi.models.student_course import StudentCourse

router = APIRouter()


@router.get("/students/{id}")
async def read_user(id: str, db: AsyncSession = Depends(get_db_async)):
    stmt = select(Student).where(Student.id == id)
    result = (await db.execute(stmt)).scalars().unique().one_or_none()
    return result


@router.get(
    "/students/{student_id}/courses",
    summary="获取某学生的所有课程",
    description="获取某学生的所有课程 desc",
)
async def get_student_courses(
    student_id: int, db: AsyncSession = Depends(get_db_async)
):
    stmt = select(Student).where(Student.id == student_id)
    result: [Student | None] = (await db.execute(stmt)).scalars().one_or_none()
    if result is None:
        return []
    return result.courses


@router.get(
    "/courses/{course_id}/students",
    summary="获取某课程的所有学生",
    description="desc",
)
async def get_course_students(course_id: int, db: AsyncSession = Depends(get_db_async)):
    stmt = select(Course).where(Course.id == course_id)
    result: [Course | None] = (await db.execute(stmt)).scalars().one_or_none()
    if result is None:
        return []
    return result.students


@router.get("/student_courses", summary="获取某图书的所有作者")
async def get_book_authors(db: AsyncSession = Depends(get_db_async)):
    book_authors = await db.execute(
        select(StudentCourse)
        # .options(joinedload(StudentCourse.columns.student))
        # .options(joinedload(BookAuthor.author))
    )
    # res = book_authors.scalars().all()
    return book_authors.scalars().all()
