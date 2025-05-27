from sqlalchemy import Identity, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, comment="学生ID")
    # id: Mapped[int] = mapped_column(Integer, autoincrement=True, comment="学生ID")  # 不推荐写法
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学生姓名")
    age: Mapped[int] = mapped_column(Integer, nullable=False, comment="学生年龄")
