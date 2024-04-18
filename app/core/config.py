import os
from pathlib import Path
from typing import Type, Tuple

from pydantic import DirectoryPath, PostgresDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, TomlConfigSettingsSource

BASE_DIR: Path = Path(__file__).resolve().parent.parent
PROJECT_DIR: Path = BASE_DIR.parent


# load_dotenv(dotenv_path=PROJECT_DIR.joinpath('.env'))

class Nest2(BaseModel):
    name: str
    ...


class NestedModel(BaseModel):
    book: Nest2
    demo: int = 12


class Settings(BaseSettings):

    @classmethod
    def load_env(cls):
        pass

    # nested_model: NestedModel
    API_V1_STR: str = "/api/v1"
    app_name: str = "demo 134"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    # use "openssl rand -hex 32" to generate a secure random secret key
    SECRET_KEY: str = "7212718542579599fe8923e3bf1632862d13f636def7d0cdd60a1765a10553d5"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = 'demo-fastapi'
    BASE_DIR: str | DirectoryPath = BASE_DIR
    PROJECT_DIR: str | DirectoryPath = BASE_DIR.parent
    PATH: str
    PATH2: str = f"2-{os.getenv('PATH', 'dev')}"
    PGUSER: str
    PGPASS: str
    # TODO set container ip
    POSTGRES_DSN: PostgresDsn | str
    # POSTGRES_DSN: str | PostgresDsn = f"postgresql://{PGUSER}:{PGPASS}@172.18.0.2:5432/demo_fastapi"
    # POSTGRES_DSN: str | PostgresDsn = f"postgresql://{PGUSER}:{PGPASS}@localhost:5432/demo_fastapi"
    log_file_path: str | DirectoryPath = BASE_DIR.joinpath("log")
    toml1: str
    nested: NestedModel

    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        extra='ignore',
        env_file=('.env', '.env.local', '.env.staging', '.env.prod'),
        toml_file='temp/config.toml'

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
        return TomlConfigSettingsSource(settings_cls), dotenv_settings, env_settings,


settings = Settings()
