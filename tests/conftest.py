from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from demo_fastapi.core.db import async_engine, engine
from demo_fastapi.main import app


@pytest.fixture(scope="module", name="client", autouse=True)
def _client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
    # return TestClient(app)


@pytest.fixture(scope="module", name="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@pytest_asyncio.fixture(scope="module", name="asession", autouse=True)
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session
