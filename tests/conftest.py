# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.schemas.base import UserCreate
from app.database import Base, get_db
from app.main import app

# --- Test SQLite DB ---
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# ------------------------------------------------------
# SHARED DB FIXTURE (unit + integration)
# ------------------------------------------------------
@pytest.fixture(scope="function")
def db():
    """Create a clean database before each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# ------------------------------------------------------
# FASTAPI Test Client (uses the above DB)
# ------------------------------------------------------
@pytest.fixture(scope="module")
def client():
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    """Secondary DB fixture used by some unit tests."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def test_user(db_session):
    """Creates and returns a sample user for relationship tests."""
    data = UserCreate(
        first_name="Test",
        last_name="User",
        email="test_user@example.com",
        username="testuser",
        password="StrongPass123"
    )

    user = User.register(db_session, data.model_dump())
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
