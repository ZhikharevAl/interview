from collections.abc import Generator
from typing import Any

from app.core.config import settings
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm.session import Session

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

engine = create_engine(
    settings.DATABASE_URL,
    **({"connect_args": {"check_same_thread": False}} if "sqlite" in settings.DATABASE_URL else {}),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata_obj = MetaData(naming_convention=naming_convention)


class Base(DeclarativeBase):
    """Base class for all database models."""

    metadata = metadata_obj


def get_db() -> Generator[Session, Any]:
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
