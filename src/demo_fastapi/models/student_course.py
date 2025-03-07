"""
学生课程表
Use sqlalchemy v2
"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .models import Base

# 关联表
# course_student_association = Table(
#     "course_student_association",
#     Base.metadata,
#     Column("course_id", ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True),
#     Column("student_id", ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
#     Column("enrolled_at", DateTime, default=datetime.utcnow, nullable=False),
# )


class Association(Base):
    __tablename__ = "association"
    student_id: Mapped[int] = mapped_column(
        ForeignKey("student.id", ondelete="CASCADE"), primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("course.id", ondelete="CASCADE"), primary_key=True
    )
    extra_data: Mapped[str | None] = mapped_column(
        String(50), nullable=True, comment="额外数据"
    )
    # student: Mapped["Student"] = relationship()
    # course: Mapped["Course"] = relationship()
    # student: Mapped["Student"] = relationship(back_populates="courses")
    # course: Mapped["Course"] = relationship(back_populates="students")


class Student(Base):
    __tablename__ = "student"
    __table_args__ = {"comment": "学生表"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, comment="学生ID"
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学生姓名")
    age: Mapped[int] = mapped_column(Integer, nullable=False, comment="学生年龄")
    courses: Mapped[list["Course"]] = relationship(
        secondary="association",
        back_populates="students",
        # back_populates="students"
    )


class Course(Base):
    __tablename__ = "course"
    __table_args__ = {"comment": "课程表"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, comment="课程ID"
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="课程名称")

    students: Mapped[list["Student"]] = relationship(
        secondary="association",
        back_populates="courses",
        # back_populates="courses"
    )
