from demo_fastapi.core.config import Settings


def test_config():
    settings = Settings()
    assert settings.API_V1_STR is not None
    assert settings.redis.host == "127.0.0.1"
