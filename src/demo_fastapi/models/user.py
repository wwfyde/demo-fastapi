from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="用户名")
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=True,
        comment="更新时间",
    )
    items = relationship("Item", back_populates="owner")
    orders = relationship("Order", back_populates="owner")  # 修改为 "Order"

    def __repr__(self):
        return f"<User(id={self.id} email={self.email}, username={self.username})>"
