from pathlib import Path
from typing import Tuple, Type

from pydantic import BaseModel, DirectoryPath, computed_field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

base_dir: Path = Path(__file__).resolve().parent.parent
project_dir: Path = base_dir.parent


# load_dotenv(dotenv_path=PROJECT_DIR.joinpath('.env'))


class Nest2(BaseModel):
    name: str
    ...


class NestedModel(BaseModel):
    book: Nest2
    demo: int = 12


class Redis(BaseModel):
    host: str
    port: int
    database: int | None = 0
    password: str | None = ""


class MySQLSettings(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str
    pool_size: int = 30
    max_overflow: int = 60


class Postgres(BaseModel):
    host: str
    port: int
    username: str
    password: str
    database: str
    pool_size: int = 30


class RabbitMQ(BaseModel):
    username: str
    password: str
    host: str
    port: int
    exchange: str
    virtual_host: str | None
    connection_name: str
    ssh: bool


class Settings(BaseSettings):
    @classmethod
    def load_env(cls):
        pass

    # nested_model: NestedModel
    api_v1_str: str = "/api/v1"
    app_name: str = "demo 134"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    # use "openssl rand -hex 32" to generate a secure random secret key
    secret_key: str = "7212718542579599fe8923e3bf1632862d13f636def7d0cdd60a1765a10553d5"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    project_name: str = "demo-fastapi"
    base_dir: str | DirectoryPath = base_dir
    project_dir: str | DirectoryPath = base_dir.parent
    redis: Redis

    # postgres
    postgres: Postgres
    mysql: MySQLSettings
    rabbitmq: RabbitMQ

    # TODO set container ip
    log_file_path: str | DirectoryPath = base_dir.joinpath("log")
    toml1: str
    nested: NestedModel
    demo: str

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        extra="ignore",
        env_file=(".env", ".env.staging", ".env.prod", ".env.local"),
        yaml_file=[
            "config.yml",
            "config.dev.yml",
            "config.staging.yml",
            "config.prod.yml",
            "config.local.yml",
            "config.dev.local.yml",
            "config.staging.local.yml",
            "config.prod.local.yml",
        ],
        yaml_file_encoding="utf-8",
        env_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            YamlConfigSettingsSource(settings_cls),
            dotenv_settings,
            env_settings,
        )

    @computed_field
    def redis_dsn(self) -> str:
        return f"redis://:{self.redis.password or ''}@{self.redis.host}:{self.redis.port}/{self.redis.database}?health_check_interval=2"

    @computed_field
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg://{self.postgres.username}:{self.postgres.password}@{self.postgres.host}:{self.postgres.port}/{self.postgres.database}"

    @computed_field
    def mysql_dsn(self) -> str:
        return f"mysql+mysqlconnector://{self.mysql.username}:{self.mysql.password}@{self.mysql.host}:{self.mysql.port}/{self.mysql.database}"

    @computed_field
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq.username}:{self.rabbitmq.password}@{self.rabbitmq.host}:{self.rabbitmq.port}/{self.rabbitmq.virtual_host or ''}?heartbeat=600&blocked_connection_timeout=300"
        # return f"amqp://{self.rabbitmq.username}:{self.rabbitmq.password}@{self.rabbitmq.host}:{self.rabbitmq.port}/{self.rabbitmq.virtual_host or ''}?name={self.rabbitmq.connection_name}"


settings = Settings()

if __name__ == "__main__":
    print(settings.demo)
    print(settings.mysql_dsn)
    print(settings.redis_dsn)
    print(settings.postgres_dsn)
