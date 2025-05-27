from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column, relationship

# dify convention
POSTGRES_NAMING = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

# https://docs.sqlalchemy.org/en/20/core/constraints.html#configuring-constraint-naming-conventions
convention = {
    "ix": "ix_%(column_0_label)s",  # index
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # foreign key
    "pk": "pk_%(table_name)s",  # primary key
}

metadata = MetaData(naming_convention=convention)


# class Base(MappedAsDataclass, DeclarativeBase):
class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata
    pass


class DateMixin(MappedAsDataclass):
    created_at: Mapped[str | None] = None
    updated_at: Mapped[str | None] = None


class CommonMixin:
    """define a series of common elements that may be applied to mapped
    classes using this class as a mixin class."""

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)


class HasLogRecord:
    """mark classes that have a many-to-one relationship to the
    ``LogRecord`` class."""

    log_record_id: Mapped[int] = mapped_column(ForeignKey("logrecord.id"))

    @declared_attr
    def log_record(self) -> Mapped["LogRecord"]:  # noqa: F821
        return relationship("LogRecord")


class PKMixin:
    pass
