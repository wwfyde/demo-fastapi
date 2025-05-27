import uuid
from typing import Any

from sqlalchemy import Integer, String, Text, UUID, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class publication(Base):
    __tablename__ = "publication"

    # Keyword arguments can be specified with the above form by specifying the last argument as a dictionary:
    __table_args__ = ({"extend_existing": True, "comment": "出版物"},)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class Artice(Base):
    __tablename__ = "article"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),  # recommended for pg13+,  server_default=text("uuid_generate_v4()"),
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False, comment="文章标题")
    author: Mapped[str] = mapped_column(String(100), nullable=False, comment="文章作者")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="文章内容")
    # 概要
    summary: Mapped[str] = mapped_column(Text, nullable=False, comment="文章概要")
    # 封面
    cover: Mapped[str] = mapped_column(String(100), nullable=False, comment="文章封面")
    # 重点：JSONB 列
    tags: Mapped[list[str]] = mapped_column(JSONB, default=list, comment="文章标签")
    extra: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, comment="文章扩展信息")


class Book(Base):
    __tablename__ = "book"
    pass


class Journal(Base):
    __tablename__ = "journal"
    pass
