import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.config import TestConfig as config
from application.database import Base, get_db
from application.main import application

SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


application.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(application)


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = next(override_get_db())
    yield db
    Base.metadata.drop_all(bind=engine)
