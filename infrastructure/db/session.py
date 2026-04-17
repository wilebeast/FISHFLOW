from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from infrastructure.config.settings import get_settings
from infrastructure.db import models  # noqa: F401


settings = get_settings()
engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
