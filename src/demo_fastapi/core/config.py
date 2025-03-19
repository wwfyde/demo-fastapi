from pathlib import Path
from typing import Final, Tuple, Type

from pydantic import (
    BaseModel,
    ConfigDict,
    DirectoryPath,
    Field,
    SecretStr,
    computed_field,
)
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

base_dir: Path = Path(__file__).resolve().parent.parent
project_dir: Path = base_dir.parent


# load_dotenv(dotenv_path=PROJECT_DIR.joinpath('.env'))


class RedisConfig(BaseModel):
    host: str
    port: int
    database: int | None = 0
    password: SecretStr | None = ""


class MySQLSettings(BaseModel):
    host: str
    port: int
    username: str
    password: SecretStr
    database: str
    pool_size: int = 30
    max_overflow: int = 60


class PostgresConfig(BaseModel):
    host: str
    port: int
    username: str
    password: SecretStr
    database: str
    pool_size: int = 30


class RabbitMQ(BaseModel):
    username: str
    password: SecretStr
    host: str
    port: int
    exchange: str
    virtual_host: str | None
    connection_name: str
    ssh: bool


class ItemConfig(BaseModel):
    name: str
    price: float
    id: str = None
    model_config = ConfigDict(
        from_attributes=True,
        strict=False,
        coerce_numbers_to_str=True,
    )


class Model(BaseModel):
    a: str
    model_config = ConfigDict(coerce_numbers_to_str=True)


class APIAnalyticsConfig(BaseSettings):
    api_key: str | None = None


class TraceConfig(BaseSettings):
    api_analytics: APIAnalyticsConfig


class Settings(BaseSettings):
    @classmethod
    def load_env(cls):
        pass

    # nested_model: NestedModel
    API_V1_STR: Final[str] = "/api/v1"
    app_name: str = "demo 134"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    # use "openssl rand -hex 32" to generate a secure random secret key
    secret_key: str = "7212718542579599fe8923e3bf1632862d13f636def7d0cdd60a1765a10553d5"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    project_name: str = "demo-fastapi"
    base_dir: str | DirectoryPath = base_dir
    project_dir: str | DirectoryPath = base_dir.parent
    redis: RedisConfig = None
    A: str = "initial"
    lists: list[ItemConfig] = None

    first_superuser_email: str = Field(default=...)
    first_superuser_username: str = Field(default="admin")
    first_superuser_password: str = Field(default=...)

    # postgres
    postgres: PostgresConfig = None
    # mysql: MySQLSettings
    # rabbitmq: RabbitMQ

    trace: TraceConfig = None

    # TODO set container ip
    log_file_path: str | DirectoryPath = base_dir.joinpath("log")

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
            env_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    @computed_field
    @property
    def redis_dsn(self) -> str:
        return f"redis://:{self.redis.password.get_secret_value() or ''}@{self.redis.host}:{self.redis.port}/{self.redis.database}?health_check_interval=2"

    @computed_field
    @property
    def postgres_dsn(self) -> str:
        return f"postgresql+psycopg://{self.postgres.username}:{self.postgres.password.get_secret_value()}@{self.postgres.host}:{self.postgres.port}/{self.postgres.database}"

    # @computed_field
    # @property
    # def mysql_dsn(self) -> str:
    #     return f"mysql+mysqlconnector://{self.mysql.username}:{self.mysql.password}@{self.mysql.host}:{self.mysql.port}/{self.mysql.database}"

    # @computed_field
    # @property
    # def rabbitmq_url(self) -> str:
    #     return f"amqp://{self.rabbitmq.username}:{self.rabbitmq.password}@{self.rabbitmq.host}:{self.rabbitmq.port}/{self.rabbitmq.virtual_host or ''}?heartbeat=600&blocked_connection_timeout=300"
    #     # return f"amqp://{self.rabbitmq.username}:{self.rabbitmq.password}@{self.rabbitmq.host}:{self.rabbitmq.port}/{self.rabbitmq.virtual_host or ''}?name={self.rabbitmq.connection_name}"


settings = Settings()


class ExtraSettings(BaseSettings):
    B: str = "global"

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=(".extra-env", ".extra-env.staging", ".env.prod", ".extra-env.local"),
        env_ignore_empty=True,
        env_file_encoding="utf-8",
    )


extra_settings = ExtraSettings()


class GlobalSettings(BaseModel):
    default: Settings = settings
    extra: ExtraSettings = extra_settings


global_settings = GlobalSettings()


if __name__ == "__main__":
    print(settings.redis_dsn)
    print(settings.postgres_dsn)
    print(settings.A)
    print(settings.API_V1_STR)
    print(settings.lists)
    print(type(settings.lists[0].id))
    print(global_settings.default.A)
    print(global_settings.extra.B)
