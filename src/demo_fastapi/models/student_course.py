"""
学生课程表
Use sqlalchemy v2
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

# 关联表
student_course = Table(
    "student_course",
    Base.metadata,
    Column(
        "course_id",
        ForeignKey("course.id", ondelete="CASCADE"),
        primary_key=True,
        comment="课程ID",
    ),
    Column(
        "student_id",
        ForeignKey("student.id", ondelete="CASCADE"),
        primary_key=True,
        comment="学生ID",
    ),
    Column(
        "enrolled_at",
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="报名时间",
    ),
    comment="学生课程表",
)
StudentCourse = student_course


class Student(Base):
    __tablename__ = "student"
    __table_args__ = {"comment": "学生表"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="学生ID")
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学生姓名")
    age: Mapped[int] = mapped_column(Integer, nullable=False, comment="学生年龄")
    courses: Mapped[list["Course"]] = relationship(secondary=student_course, back_populates="students", lazy="selectin")


class Course(Base):
    __tablename__ = "course"
    __table_args__ = {"comment": "课程表"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="课程ID")
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="课程名称")

    students: Mapped[list["Student"]] = relationship(
        secondary=student_course, back_populates="courses", lazy="selectin"
    )
