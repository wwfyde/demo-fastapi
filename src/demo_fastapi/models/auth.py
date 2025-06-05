from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, DateMixin


class Token(Base, DateMixin):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="令牌ID")
    access_token: Mapped[str | None] = mapped_column(nullable=False, comment="访问令牌")
    expired_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=True,
        comment="更新时间",
    )
    # scope = (String, nullable=False, default="read")
