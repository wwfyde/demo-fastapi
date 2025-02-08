from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .models import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), index=True)
    description = Column(String(1024), nullable=True)
    description2 = Column(String(1024), nullable=True)
    config = Column(JSON, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # name_alias = mapped_column(String(64), name='alias')

    owner = relationship("User", back_populates="items")
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

    def __repr__(self):
        return f"<Item id={self.id} title={self.title}, {self.description=}>"
