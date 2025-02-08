import time

from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.db import async_engine
from src.models import Item


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
                    "description": "Description",
                    "description2": "Description2",
                    "config": {"key": "value"},
                    "owner_id": 1,
                }
                # Item(title=f"Item {i}", description="Description", description2="Description2", config={"key": "value"},
                #      owner_id=1)
                for i in range(5000, 10000)
            ]

            start_time = time.time()

            stmt = insert(Item).values(items)
            await session.execute(stmt)
            await session.commit()
            end_time = time.time()
            print(f"execute_insert took {end_time - start_time} seconds")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
