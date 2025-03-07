from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .models import Base


class Order(Base):
    __tablename__ = "order"  # 修改表名为 "order"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(128), unique=True, index=True)
    description = Column(String(256), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=True,
    )

    # Assuming there is a relationship with User model
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="orders")
