from sqlalchemy import Column, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, relationship

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

    def __repr__(self):
        return f"<Item id={self.id} title={self.title}, {self.description=}>"