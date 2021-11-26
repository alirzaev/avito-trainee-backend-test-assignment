import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.config import get_config
from application.database import Base, get_db
from application.asgi import application

config = get_config()

SQLALCHEMY_DATABASE_URL = config.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    try:
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db
    
    application.dependency_overrides[get_db] = override_get_db
    yield TestClient(application)
    del application.dependency_overrides[get_db]


@pytest.fixture
def ad_sample_input():
    return {
        'name': "Ad's name",
        'description': "Ad's description",
        'price': 100,
        'photos': [
            {
                'url': 'http://example.com/1.jpg'
            },
            {
                'url': 'http://example.com/2.jpg'
            }
        ]
    }
