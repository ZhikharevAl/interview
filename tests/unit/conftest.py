from collections.abc import Generator

import pytest
from app.db.database import Base
from app.schemas.category import CategoryCreate
from app.services import category as category_service
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def db_session() -> Generator[Session]:
    """Create a database session for unit testing."""
    Base.metadata.create_all(bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def sample_category(db_session: Session) -> category_service.CategoryModel:
    """Create a sample category for questions."""
    category_data = CategoryCreate(name="Test Category")
    return category_service.create_category(db_session, category_data)
