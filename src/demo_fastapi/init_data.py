import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from demo_fastapi.core.config import settings
from demo_fastapi.core.db import async_engine
from demo_fastapi.core.security import get_password_hash
from demo_fastapi.models import User


async def runner():
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            user = await session.execute(
                select(User).where(User.email == settings.first_superuser_email)
            )
            user = user.fetchone()
            print(user)
            if not user:
                # user_in = UserCreate(
                #     email=settings.first_superuser_email,
                #     username=settings.first_superuser_username,
                #     password=get_password_hash(settings.first_superuser_password),
                #     is_superuser=True,
                # )

                user_in = User(
                    email=settings.first_superuser_email,
                    username=settings.first_superuser_username,
                    hashed_password=get_password_hash(
                        settings.first_superuser_password
                    ),
                    is_superuser=True,
                )

                session.add(user_in)
                logging.warning("创建管理员用户成功")

                pass
                # await session.aclose()
            else:
                logging.warning("用户已创建, 无需再创建")


def main():
    import asyncio

    asyncio.run(runner())


if __name__ == "__main__":
    main()
