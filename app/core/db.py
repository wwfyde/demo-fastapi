from sqlalchemy import create_engine

from app import settings

# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import create_async_engine

# from app.core.config import settings


# asyncio_engine = create_async_engine(
#     "postgresql+psycopg_async://<user>:<pass>@localhost/<db>", connect_args={}, echo=True)
engine = create_engine(str(settings.POSTGRES_DSN), connect_args={}, echo=True)
