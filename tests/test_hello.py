import pytest
from starlette.testclient import TestClient

from demo_fastapi.main import app


@pytest.fixture(name="client", scope="module")
def _client():
    return TestClient(app)


def test_hello(client):
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, 世界!"}
