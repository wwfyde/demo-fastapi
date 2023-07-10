from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.POSTGRES_DSN, echo=True)
SessionLocal = sessionmaker(autoflush=False, bind=engine)