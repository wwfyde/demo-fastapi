from datetime import datetime
from typing import Literal

from sqlalchemy import (
    JSON,
    TIMESTAMP,
    BigInteger,
    Boolean,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

type CategoryType = Literal["women", "men", "girls", "boys", "other"]


class Product(Base):
    __tablename__ = "product"
    __table_args__ = (
        Index("ix_source_product_id", "source", "product_id"),
        # Index("ix_source_product_id_sku_id", "source", "product_id", "sku_id"),  # 组合索引
        Index("ix_review_count", "review_count"),
        Index("ix_product_id", "product_id"),
        UniqueConstraint("product_id", "source", name="uq_product_id_source"),
        {"comment": "商品"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="内部ID")  # 内部ID
    product_id: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="商品ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="商品名称")
    primary_sku_id: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="主SKU ID, 部分系统可用")
    brand: Mapped[str | None] = mapped_column(String(64), comment="品牌")
    product_url: Mapped[str | None] = mapped_column(String(1024), comment="商品链接")
    rating: Mapped[float | None] = mapped_column(Numeric(2, 1), nullable=True, comment="评分")
    review_count: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0, comment="评论数")
    rating_count: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0, comment="评分数")

    attributes: Mapped[dict | None] = mapped_column(JSON, comment="额外商品属性, 特点, 和描述bulletedCopyAttrs")
    description: Mapped[str | None] = mapped_column(String(1024), comment="描述")
    attributes_raw: Mapped[dict | list | None] = mapped_column(JSON, comment="原始属性")
    category: Mapped[CategoryType | None] = mapped_column(String(256), comment="商品类别")

    gender: Mapped[Literal["F", "M", "O"]] = mapped_column(String(16), nullable=True, comment="性别")
    released_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True, index=True, comment="上新时间"
    )
    tags: Mapped[list[str] | None] = mapped_column(JSON, comment="标签")
    current_version: Mapped[str | None] = mapped_column(String(32), default="0", comment="当前版本")
    is_review_analyzed: Mapped[bool | None] = mapped_column(Boolean, default=False, comment="是否已分析")
    review_analyses: Mapped[list[dict] | None] = mapped_column(JSON, comment="评论分析结果汇总")
    extra_review_analyses: Mapped[list[dict] | None] = mapped_column(JSON, comment="额外评论分析结果汇总")
    extra_metrics: Mapped[list | dict | None] = mapped_column(JSON, comment="额外评论指标")
    review_statistics: Mapped[dict | None] = mapped_column(JSON, comment="评论分析统计")
    extra_review_statistics: Mapped[dict | None] = mapped_column(JSON, comment="额外评论分析统计")
    review_summary: Mapped[dict | list | None] = mapped_column(JSON, comment="评论总结")

    remark: Mapped[str | None] = mapped_column(String(1024), comment="备注")
    category_id: Mapped[int | None] = mapped_column(BigInteger, comment="类别ID")
    is_deleted: Mapped[bool | None] = mapped_column(Boolean, default=False, comment="软删除")
    gathered_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        comment="采集时间",
    )
    last_gathered_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        comment="最近采集时间",
        onupdate=func.now(),
    )
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )
    # skus = relationship("ProductSKU",
    #                     primaryjoin="Product.product_id == ProductSKU.product_id and Product.source == ProductSKU.source",
    #                     back_populates="product")


class ProductTranslation(Base):
    __tablename__ = "product_translation"
    __table_args__ = (
        Index("ix_source_product_id", "source", "product_id"),
        {"comment": "商品翻译"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="内部ID")
    language_code: Mapped[Literal["zh", "en"]] = mapped_column(String(16), nullable=False, default="zh", comment="语言")
    product_id: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="商品ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="商品名称")
    brand: Mapped[str | None] = mapped_column(String(64), comment="品牌")
    attributes: Mapped[dict | None] = mapped_column(JSON, comment="额外商品属性, 特点, 和描述bulletedCopyAttrs")
    description: Mapped[str | None] = mapped_column(String(1024), comment="描述")
    attributes_raw: Mapped[dict | list | None] = mapped_column(JSON, comment="原始属性")
    category: Mapped[CategoryType | None] = mapped_column(String(256), comment="商品类别")
    gender: Mapped[Literal["F", "M", "O"]] = mapped_column(String(16), nullable=True, comment="性别")
    tags: Mapped[list[str] | None] = mapped_column(JSON, comment="标签")
    review_analyses: Mapped[list[dict] | None] = mapped_column(JSON, comment="评论分析结果汇总")
    extra_review_analyses: Mapped[list[dict] | None] = mapped_column(JSON, comment="额外评论分析结果汇总")
    extra_metrics: Mapped[list | dict | None] = mapped_column(JSON, comment="额外评论指标")
    review_statistics: Mapped[dict | None] = mapped_column(JSON, comment="评论分析统计")
    extra_review_statistics: Mapped[dict | None] = mapped_column(JSON, comment="额外评论分析统计")
    review_summary: Mapped[str | None] = mapped_column(String(2048), comment="评论总结")
    remark: Mapped[str | None] = mapped_column(String(1024), comment="备注")
    category_id: Mapped[int | None] = mapped_column(BigInteger, comment="类别ID")
    is_deleted: Mapped[bool | None] = mapped_column(Boolean, default=False, comment="软删除")
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )


class ProductDetail(Base):
    __tablename__ = "product_detail"
    __table_args__ = (
        Index("ix_source_product_id", "source", "product_id"),
        UniqueConstraint("product_id", "source", name="uq_product_id_source"),
        {"comment": "商品"},
    )
    id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True, comment="内部ID")
    product_id: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="商品ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )

    # style: Mapped[str | None] = mapped_column(String(64), comment="款式")  # deprecated 对应 商品名称name
    # style_number: Mapped[str | None] = mapped_column(String(64), comment="款号")  # deprecated 对应product_id
    # source_id: Mapped[int | None] = mapped_column(BigInteger, comment="源商品ID")
    store: Mapped[str | None] = mapped_column(String(64), comment="所属商店")

    # 固定属性

    material: Mapped[str | None] = mapped_column(String(128), comment="材质")  # 固定属性
    neckline: Mapped[str | None] = mapped_column(String(128), comment="领口")  # 固定属性
    fabric: Mapped[str | None] = mapped_column(String(128), comment="面料名称")  # 固定属性
    origin: Mapped[str | None] = mapped_column(String(128), comment="产地")  # 固定属性
    length: Mapped[str | None] = mapped_column(String(128), comment="服装长度")  # 固定属性
    fit: Mapped[str | None] = mapped_column(String(128), comment="合身度")  # 固定属性
    vendor: Mapped[str | None] = mapped_column(String(64), comment="供应商")
    clothing_details: Mapped[str | None] = mapped_column(String(1024), comment="服装细节")
    package_quantity: Mapped[int | None] = mapped_column(Integer, comment="包装数量")
    care_instructions: Mapped[str | None] = mapped_column(String(1024), comment="护理和清洁")
    raw_data: Mapped[dict | None] = mapped_column(JSON, comment="原始数据, json字段")
    parent_category: Mapped[str | None] = mapped_column(String(256), comment="父商品类别")
    category_breadcrumbs: Mapped[str | None] = mapped_column(String(1024), comment="商品类别级联")
    main_category: Mapped[str | None] = mapped_column(String(256), comment="主类别, 用于抓取时类别标识")
    sub_category: Mapped[str | None] = mapped_column(String(256), comment="子类别, 用于抓取时类别标识")
    lot_id: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="产品批次 ID")


class ProductSKU(Base):
    __tablename__ = "product_sku"
    __table_args__ = (
        Index("ix_source_sku_id", "source", "sku_id", mysql_using="hash"),
        Index("ix_source_product_id", "source", "product_id", mysql_using="hash"),
        Index("ix_product_id", "product_id"),
        UniqueConstraint("product_id", "sku_id", "source", name="uq_product_id_sku_id_source"),
        {"comment": "商品SKU"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="内部ID")
    sku_id: Mapped[str | None] = mapped_column(String(128), comment="源SKU ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_id: Mapped[str | None] = mapped_column(String(128), comment="商品ID")

    size: Mapped[str | None] = mapped_column(String(64), comment="尺码")
    color: Mapped[str | None] = mapped_column(String(64), comment="颜色")
    material: Mapped[str | None] = mapped_column(String(128), comment="材质")
    # source_id: Mapped[int | None] = mapped_column(BigInteger, comment="源商品ID")
    sku_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="SKU名称")
    product_url: Mapped[str | None] = mapped_column(String(1024), comment="商品链接")
    image_url: Mapped[str | None] = mapped_column(String(512), nullable=True, comment="商品图片")
    outer_image_url: Mapped[str | None] = mapped_column(String(1024), comment="商品图片外链")
    model_image_urls: Mapped[list[str] | None] = mapped_column(JSON, comment="模特图片链接列表")
    outer_model_image_urls: Mapped[list[str] | None] = mapped_column(JSON, comment="外部模特图片链接列表")
    # model_image_url: Mapped[str | None] = mapped_column(String(1024), comment="模特图片链接")
    # outer_model_image_url: Mapped[str | None] = mapped_column(String(1024), comment="外部模特图片链接")

    # style: Mapped[str | None] = mapped_column(String(128), comment="服装风格")
    inventory: Mapped[int | None] = mapped_column(Integer, comment="库存")
    inventory_status: Mapped[str | None] = mapped_column(String(32), comment="库存状态")
    # fit: Mapped[str | None] = mapped_column(String(128), comment="适合人群")
    # origin: Mapped[str | None] = mapped_column(String(128), comment="产地")

    # 其他数据
    # length: Mapped[str | None] = mapped_column(String(128), comment="服装长度")
    # neckline: Mapped[str | None] = mapped_column(String(128), comment="领口")
    # fabric_name: Mapped[str | None] = mapped_column(String(128), comment="面料名称")
    # clothing_details: Mapped[str | None] = mapped_column(String(1024), comment="服装细节")
    # package_quantity: Mapped[int | None] = mapped_column(Integer, comment="包装数量")
    # care_instructions: Mapped[str | None] = mapped_column(String(1024), comment="护理和清洁")
    is_deleted: Mapped[bool | None] = mapped_column(Boolean, default=False, comment="软删除")
    # attributes: Mapped[dict | None] = mapped_column(
    #     JSON, comment="额外SKU属性, 特征"
    # )
    # attributes_raw: Mapped[dict | list | None] = mapped_column(JSON, comment="原始属性")
    gathered_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="抓取时间",
    )
    last_gathered_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="最近抓取时间",
    )
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
        nullable=True,
        comment="更新时间",
    )
    # product: Mapped[list["Product"]] = relationship("Product",
    #                                                 primaryjoin="ProductSKU.product_id == Product.product_id and ProductSKU.source == Product.source",
    #                                                 back_populates="skus")


class ProductSKUTranslation(Base):
    __tablename__ = "product_sku_translation"
    __table_args__ = (
        Index("ix_source_sku_id", "source", "sku_id"),
        {"comment": "商品SKU翻译"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="内部ID")
    sku_id: Mapped[str | None] = mapped_column(String(128), comment="源SKU ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_id: Mapped[str | None] = mapped_column(String(128), comment="商品ID")
    language_code: Mapped[Literal["zh", "en"]] = mapped_column(
        String(16), nullable=False, default="zh", comment="语言代码"
    )
    size: Mapped[str | None] = mapped_column(String(64), comment="尺码")
    color: Mapped[str | None] = mapped_column(String(64), comment="颜色")
    material: Mapped[str | None] = mapped_column(String(128), comment="材质")
    sku_name: Mapped[str | None] = mapped_column(String(128), nullable=True, comment="SKU名称")


class ProductSKUDetail(Base):
    __tablename__ = "product_sku_detail"
    __table_args__ = (
        Index("ix_source_sku_id", "source", "sku_id"),
        UniqueConstraint("product_id", "sku_id", "source", name="uq_product_id_sku_id_source"),
        {"comment": "商品SKU详情"},
    )
    id: Mapped[int] = mapped_column(ForeignKey("product_sku.id"), primary_key=True, comment="内部ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    sku_id: Mapped[str | None] = mapped_column(String(128), comment="源SKU ID")
    product_id: Mapped[str | None] = mapped_column(String(128), comment="商品ID")


class ProductReview(Base):
    __tablename__ = "product_review"
    __table_args__ = (
        Index("ix_source_product_id", "source", "product_id"),
        Index("ix_source_product_id", "source", "product_id", "review_id"),
        UniqueConstraint("review_id", "product_id", "source", name="uq_review_id_product_id_source"),
        {"comment": "商品评论"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    review_id: Mapped[str | None] = mapped_column(String(64), comment="源评论ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="商品ID")
    current_version: Mapped[str | None] = mapped_column(String(32), default="0", comment="当前版本")
    sku_id: Mapped[str | None] = mapped_column(String(64), comment="SKU ID")
    rating: Mapped[float | None] = mapped_column(
        Numeric(2, 1), comment="评分"
    )  # CheckConstraint('rating >= 1 AND rating <= 5'
    title: Mapped[str | None] = mapped_column(String(1024), comment="评论标题")
    comment: Mapped[str | None] = mapped_column(Text, comment="评论内容")
    photos: Mapped[list[str] | None] = mapped_column(JSON, comment="评论图片")
    outer_photos: Mapped[list[str] | None] = mapped_column(JSON, comment="评论外部数据源")
    nickname: Mapped[str | None] = mapped_column(String(64), comment="昵称")
    helpful_votes: Mapped[int | None] = mapped_column(Integer, default=0, comment="按顶票数")
    not_helpful_votes: Mapped[int | None] = mapped_column(Integer, comment="按踩票数")
    is_deleted: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True, comment="软删除")
    gathered_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="内部创建时间",
    )
    last_gathered_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=True,
        comment="内部更新时间",
    )
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="更新时间",
    )


class ProductReviewTranslation(Base):
    __tablename__ = "product_review_translation"
    __table_args__ = (
        Index("ix_source_product_id", "source", "product_id"),
        Index("ix_source_review_id", "source", "review_id"),
        {"comment": "商品评论翻译"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    review_id: Mapped[str | None] = mapped_column(String(64), comment="源评论ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="商品ID")
    sku_id: Mapped[str | None] = mapped_column(String(64), comment="SKU ID, 部分系统支持sku_id区分")
    language_code: Mapped[Literal["zh", "en"]] = mapped_column(
        String(16), nullable=False, default="zh", comment="语言代码"
    )
    title: Mapped[str | None] = mapped_column(String(1024), comment="评论标题")
    comment: Mapped[str | None] = mapped_column(Text, comment="评论内容")
    is_deleted: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True, comment="软删除")
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        comment="更新时间",
    )


class ProductReviewAnalysis(Base):
    __tablename__ = "product_review_analysis"
    __table_args__ = (
        Index("ix_source_review_id", "source", "review_id"),
        Index("ix_source_review_id_version_id", "source", "review_id", "version_id"),
        {"comment": "商品评论分析, 支持版本号管理"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    review_id: Mapped[str | None] = mapped_column(String(64), comment="源评论ID")
    version_id: Mapped[str | None] = mapped_column(String(32), default="0", comment="版本ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="商品ID")
    metrics: Mapped[dict | list | None] = mapped_column(JSON, comment="评论指标")
    quality: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品质量指标")
    warmth: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品保暖性指标")
    comfort: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品舒适度指标")
    softness: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品柔软性指标")
    preference: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品偏好指标")
    repurchase_intent: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品回购意愿指标")
    appearance: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品外观指标")
    fit: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="商品合身度指标")
    extra_metrics: Mapped[dict | list | None] = mapped_column(JSON, comment="额外评论指标")
    token_usage: Mapped[dict | list | None] = mapped_column(JSON, comment="LLM token 消耗")
    is_deleted: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True, comment="软删除")
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="更新时间",
    )


class ReviewAnalysisExtraMetric(Base):
    __tablename__ = "review_analysis_extra_metric"
    __table_args__ = (
        Index("ix_source_review_id", "source", "review_id"),
        # Index("ix_source_product_id_version_id", "source", "product_id", "version_id"),
        Index("ix_source_review_id_version_id", "source", "review_id", "version_id"),
        Index(
            "ix_source_review_id_version_id_name",
            "source",
            "review_id",
            "version_id",
            "name",
        ),
        {"comment": "商品评论额外指标, 支持版本管理"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, comment="ID")
    review_id: Mapped[str | None] = mapped_column(String(64), comment="源评论ID")
    source: Mapped[Literal["gap", "target", "next", "jcpenney", "other"]] = mapped_column(
        String(64), default="other", nullable=True, comment="数据来源"
    )
    product_id: Mapped[str | None] = mapped_column(String(64), nullable=True, comment="商品ID")
    version_id: Mapped[str | None] = mapped_column(String(32), default="0", comment="版本ID")
    name: Mapped[str | None] = mapped_column(String(64), comment="指标名称")
    value: Mapped[float | None] = mapped_column(Numeric(3, 1), default=0, comment="指标得分")
    created_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="创建时间",
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=True,
        comment="更新时间",
    )
