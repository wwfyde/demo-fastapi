from datetime import datetime

from sqlalchemy import Integer, String, JSON, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .models import Base


class LLM(Base):
    __tablename__ = "llm"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False, comment="模型名称")
    description: Mapped[str | None] = mapped_column(String(1024), comment="详细说明")
    provider: Mapped[str | None] = mapped_column(String(32), comment='供应商, 渠道名称')
    base_url: Mapped[str | None] = mapped_column(String(512), comment='基础URL')
    api_key: Mapped[str | None] = mapped_column(String(128), comment='API Key')
    access_key: Mapped[str | None] = mapped_column(String(128), comment='Access Key for AWS bedrock')
    secret_key: Mapped[str | None] = mapped_column(String(128), nullable=True, comment='Secret Key for AWS bedrock')
    model: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='默认模型')
    model_extra: Mapped[list[str] | None] = mapped_column(JSON, nullable=True, comment="模型列表")
    config: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="配置列表")
    status: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=True, comment='渠道状态')
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False, comment='是否删除')
    expire_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment='过期时间')
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=func.now(),
                                                        server_default=func.now(), nullable=True, comment='创建时间')
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=func.now(), onupdate=func.now(),
                                                        server_default=func.now(), server_onupdate=func.now(),
                                                        nullable=True, comment='更新时间')
