import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from pydantic import DirectoryPath, PostgresDsn
from pydantic_settings import BaseSettings

BASE_DIR: Path = Path(__file__).resolve().parent.parent
PROJECT_DIR: Path = BASE_DIR.parent
load_dotenv(dotenv_path=PROJECT_DIR.joinpath('.env'))


class Settings(BaseSettings):

    @classmethod
    def load_env(cls):
        pass

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = 'demo-fastapi'
    BASE_DIR: str | DirectoryPath = BASE_DIR
    PROJECT_DIR: str | DirectoryPath = BASE_DIR.parent
    PGUSER: str = os.getenv('PGUSER')
    PGPASS: str = os.getenv('PGPASS')
    POSTGRES_DSN: str | PostgresDsn = f"postgresql://{PGUSER}:{PGPASS}@localhost:5432/demo_fastapi"
    print(PGUSER)
    log_file_path: str | DirectoryPath = BASE_DIR.joinpath("log")
    assert PGUSER == 'postgres'


settings = Settings()
