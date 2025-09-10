import sqlite3
from collections.abc import Generator
from http import HTTPStatus
from typing import Any

import pytest
from app.core.logging_config import get_logger
from app.db.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

logger = get_logger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(
    dbapi_connection: sqlite3.Connection,
    _connection_record: Any,  # noqa: ANN401
) -> None:
    """Set PRAGMA foreign_keys=ON for SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def override_get_db() -> Generator[Session]:
    """Override database dependency for integration tests."""
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    except Exception:
        logger.exception("Error in override_get_db")
        raise
    finally:
        if db is not None:
            try:
                db.close()
            except SQLAlchemyError:
                logger.exception("Error closing the database session")


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db_session() -> Generator[Session]:
    """Create a database session for testing."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client() -> Generator[TestClient]:
    """Provide FastAPI TestClient for integration tests."""
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def sample_category(client: TestClient) -> dict:
    """Create a sample category for tests."""
    response = client.post("/api/v1/categories/", json={"name": "Test Category"})
    assert response.status_code == HTTPStatus.CREATED
    return response.json()


@pytest.fixture
def sample_question(client: TestClient, sample_category: dict) -> dict:
    """Create a sample question for tests."""
    question_data = {
        "question_text": "What is integration testing?",
        "answer_text": "Integration testing is testing combined parts of an application.",
        "category_id": sample_category["id"],
    }
    response = client.post("/api/v1/questions/", json=question_data)
    assert response.status_code == HTTPStatus.CREATED
    return response.json()
