from typing import Generator

import pytest
from starlette.testclient import TestClient

from demo_fastapi.main import app


@pytest.fixture(scope="module", name="client", autouse=True)
def _client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client





    # return TestClient(app)


def test_hello(client: TestClient):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, 世界!"}
