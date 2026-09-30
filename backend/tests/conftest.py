import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.db.init_db import init_db
from app.core.security import get_password_hash, create_access_token
from app.models.user import User

# In-memory SQLite engine for fast, isolated unit testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    init_db(session)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    user = User(
        email="testuser@example.com",
        name="Test User",
        hashed_password=get_password_hash("Password123!"),
        preferred_currency="USD",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict:
    token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_user2(db: Session) -> User:
    user = User(
        email="otheruser@example.com",
        name="Other User",
        hashed_password=get_password_hash("Password123!"),
        preferred_currency="EUR",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers_user2(test_user2: User) -> dict:
    token = create_access_token(subject=test_user2.id)
    return {"Authorization": f"Bearer {token}"}
