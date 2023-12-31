from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import settings
# from app.core.config import settings
from app.core.config2 import postgres_dsn

dsn = settings.POSTGRES_DSN

# asyncio_engine = create_async_engine(
#     "postgresql+psycopg_async://postgres:wawawa@localhost/test", connect_args={}, echo=True)
engine = create_engine(dsn, connect_args={}, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
