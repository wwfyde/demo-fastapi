from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models import Student

router = APIRouter()


@router.get("/students/{id}")
async def read_user(id: str, db: Session = Depends(get_db)):
    stmt = select(Student).where(Student.id == id)
    result = db.execute(stmt).scalars().one_or_none()

    return result
