import asyncio
import json
from typing import Mapping

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src import settings


# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import create_async_engine

# from app.core.config import settings


def dumps(obj: Mapping) -> str:
    # return orjson.dumps(obj, option=orjson.OPT_SORT_KEYS | orjson.OPT_NON_STR_KEYS).decode('utf-8')
    return json.dumps(obj, sort_keys=True, ensure_ascii=True, separators=(",", ":"))


# asyncio_engine = create_async_engine(
#     "postgresql+psycopg_async://<user>:<pass>@localhost/<db>", connect_args={}, echo=True)
engine = create_engine(
    settings.postgres_dsn,
    connect_args={},
    # echo=True,
    json_serializer=dumps,
    pool_size=settings.postgres.pool_size,  # 连接池的大小
    max_overflow=60,  # 连接池中允许的最大溢出连接数量
    pool_recycle=3600,  # 在指定秒数后回收连接
    pool_pre_ping=True,  # 启用 pre_ping 参数
)
# engine = create_engine(str(settings.MYSQL_DSN), connect_args={}, echo=True)

# asyncio_engine = create_async_engine(settings.postgres_dsn)
async_engine = create_async_engine(
    settings.postgres_dsn,
    connect_args={},
    pool_size=settings.postgres.pool_size,  # 连接池的大小
    max_overflow=60,  # 连接池中允许的最大溢出连接数量
    pool_recycle=3600,  # 在指定秒数后回收连接
    pool_pre_ping=True,  # 启用 pre_ping 参数
    # echo=True,
    # json_serializer=dumps,
)

if __name__ == "__main__":

    async def main():
        async_session = async_sessionmaker(async_engine, expire_on_commit=False)
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(text("select version()"))

                print(result.scalar_one_or_none())
                pass
        # await asyncio_engine.dispose()

    asyncio.run(main())

    # async with AsyncSession(asyncio_engine) as session:
    #     async with session.begin():
    #         pass
