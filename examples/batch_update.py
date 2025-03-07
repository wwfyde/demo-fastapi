import time

from sqlalchemy import bindparam, text, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from demo_fastapi.core.db import async_engine
from demo_fastapi.models import Item


async def main():
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(text("select version()"))

            print(result.scalar_one_or_none())
            pass
            items = [
                {
                    "title": f"Item {i}",
                    "description": "Description新的描述",
                    "description2": "新的描述2",
                    "config": {"key": "value"},
                    "id": i,
                    "owner_id": 1,
                }
                # Item(title=f"Item {i}", description="Description", description2="Description2", config={"key": "value"},
                #      owner_id=1)
                for i in range(5000, 10000)
            ]

            start_time = time.time()
            kwargs = {key: bindparam(key) for key in items[0].keys()}
            print(kwargs)
            stmt = (
                update(Item)
                .where(Item.id == bindparam("id"))
                .values(**kwargs)
                .execution_options(synchronize_session=False)
            )
            await session.execute(stmt, items)
            await session.commit()
            end_time = time.time()
            print(f"execute_insert took {end_time - start_time} seconds")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
