import logging

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from demo_fastapi.core.db import async_engine
from demo_fastapi.models import User


@pytest.mark.asyncio()
async def test_get_user():
    async with AsyncSession(async_engine) as session:
        stmt = select(User).where(User.email == "admin@example.com")
        result = await session.execute(stmt)
        r: User | None = result.scalars().one_or_none()
        if r:
            print(r)
            print(r.username)
            assert r.username == "admin"
            # assert result.scalar_one_or_none() == "admin"
        else:
            logging.warning("no user")


@pytest.mark.asyncio
async def test_get_user_with_fixture(asession: AsyncSession):
    async with asession:
        stmt = select(User).where(User.email == "admin@example.com")
        result = await asession.execute(stmt)
        r: User | None = result.scalars().one_or_none()
        if r:
            print(r)
            print(r.username)
            assert r.username == "admin"
            # assert result.scalar_one_or_none() == "admin"
        else:
            logging.warning("no user")
