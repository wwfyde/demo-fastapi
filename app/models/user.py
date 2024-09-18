from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
