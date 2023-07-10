import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).resolve().parent.parent
PROJECT_DIR: Path = BASE_DIR.parent
load_dotenv(dotenv_path=PROJECT_DIR.joinpath('.env'))
PGUSER: str = os.getenv('PGUSER')
PGPASS: str = os.getenv('PGPASS')
postgres_dsn: str = f"postgresql+psycopg://{PGUSER}:{PGPASS}@localhost:5432/demo_fastapi"
