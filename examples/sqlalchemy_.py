# from sqlalchemy.ext.asyncio import create_async_engine
# asyncio_engine = create_async_engine("postgresql+psycopg_async://postgres:wawawa@localhost/test", )

from sqlalchemy.ext.asyncio import create_async_engine

asyncio_engine = create_async_engine("postgresql+psycopg_async://postgres:wawawa@localhost/test")
