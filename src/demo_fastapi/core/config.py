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
    TomlConfigSettingsSource,
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
    price: float | None = None
    id: str = None
    model_config = ConfigDict(
        from_attributes=True,
        strict=False,
        coerce_numbers_to_str=True,
    )


class AliyunOssConfig(BaseModel):
    endpoint: str
    access_key: str
    access_secret: str
    bucket_name: str
    domain: str | None = None
    ...


class Model(BaseModel):
    a: str
    model_config = ConfigDict(coerce_numbers_to_str=True)


class APIAnalyticsConfig(BaseSettings):
    api_key: str | None = None


class TraceConfig(BaseSettings):
    api_analytics: APIAnalyticsConfig | None = None


class Settings(BaseSettings):
    @classmethod
    def load_env(cls):
        pass

    # nested_model: NestedModel
    api_prefix: Final[str] = "/api/v1"
    api_key_header: Final[str] = "fullspeed"
    app_name: str = "demo-fastapi"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    # use "openssl rand -hex 32" to generate a secure random secret key
    secret_key: str = "7212718542579599fe8923e3bf1632862d13f636def7d0cdd60a1765a10553d5"
    jwt_algorithm: str = "HS256"
    access_token_expire_days: int = 30
    project_name: str = "demo-fastapi"
    project_root: str | DirectoryPath = base_dir.parent
    base_dir: str | DirectoryPath = base_dir
    project_dir: str | DirectoryPath = base_dir.parent
    redis: RedisConfig = None
    products: list[ItemConfig] | None = None

    first_superuser_email: str = Field(default=...)
    first_superuser_username: str = Field(default="admin")
    first_superuser_password: str = Field(default=...)

    # 阿里云OSS
    oss: AliyunOssConfig = None

    # postgres
    postgres: PostgresConfig = None
    # mysql: MySQLSettings
    # rabbitmq: RabbitMQ

    trace: TraceConfig | None = None

    # TODO set container ip
    log_file_path: str | DirectoryPath = base_dir.joinpath("log")

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        extra="ignore",
        env_file=(
            ".env",
            ".env.dev",
            ".env.staging",
            ".env.prod",
            ".env.local",
            ".env.dev.local",
            ".env.staging.local",
            ".env.prod.local",
        ),
        toml_file=[
            "config.toml",
            "config.dev.toml",
            "config.staging.toml",
            "config.prod.toml",
            "config.local.toml",
            "config.dev.local.toml",
            "config.staging.local.toml",
            "config.prod.local.toml",
        ],
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
        # env_nested_max_split=2,
        env_nested_delimiter="__",
        # env_prefix="DEMO_FASTAPI_",  # 环境变量前缀
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
        # The order of the returned callables decides the priority of inputs; first item is the highest priority.
        # 第一个优先级最高
        return (
            env_settings,
            dotenv_settings,
            # YamlConfigSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
        )

    @computed_field
    @property
    def redis_dsn(self) -> str:
        return f"redis://:{self.redis.password.get_secret_value() or ''}@{self.redis.host}:{self.redis.port}/{self.redis.database}?health_check_interval=2"

    @computed_field
    @property
    def postgres_dsn(self) -> str:
        # return f"postgresql+psycopg://{self.postgres.username}:{self.postgres.password.get_secret_value()}@{self.postgres.host}:{self.postgres.port}/{self.postgres.database}"
        return f"postgresql+asyncpg://{self.postgres.username}:{self.postgres.password.get_secret_value()}@{self.postgres.host}:{self.postgres.port}/{self.postgres.database}"

    @computed_field
    @property
    def postgres_dsn_sync(self) -> str:
        # return f"postgresql+psycopg://{self.postgres.username}:{self.postgres.password.get_secret_value()}@{self.postgres.host}:{self.postgres.port}/{self.postgres.database}"
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
    print(settings.api_prefix)
    print(settings.products)
    print(type(settings.products[0].id))
    print(global_settings.extra.B)
