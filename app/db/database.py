from functools import lru_cache
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import get_settings


def _build_database_url() -> str:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not configured.")
    return settings.database_url


@lru_cache(maxsize=1)
def get_engine():
    """Create and cache the SQLAlchemy engine."""

    return create_engine(_build_database_url(), pool_pre_ping=True)


@lru_cache(maxsize=1)
def get_session_factory():
    """Create and cache the SQLAlchemy session factory."""

    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for FastAPI dependencies."""

    db = get_session_factory()()
    try:
        yield db
    finally:
        db.close()
