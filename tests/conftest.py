import pytest
from fastapi.testclient import TestClient
import io
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

test_user_data = {
    "username": "testuser",
    "password": "Password123!"
}


@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides = {get_db: override_get_db}

    with TestClient(app) as c:
        yield c

    app.dependency_overrides = {}


@pytest.fixture
def auth_token(client):
    client.post("/users/register", json=test_user_data)

    response = client.post(
        "/users/login",
        data={"username": test_user_data["username"], "password": test_user_data["password"]}
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def log_file():
    content = io.BytesIO(b"2023-01-01 12:00:00 ERROR Test error message\n2023-01-01 12:01:00 INFO Test info message")
    return "files", ("log.txt", content, "text/plain")


class MockLogClient:
    def process_upload(self, file, user_id):
        return True

    def search_user_logs(self, user_id, start_time, end_time, keyword, level):
        return {
            'hits': {
                'total': {'value': 2},
                'hits': [
                    {'_source': {'timestamp': '2023-01-01 12:00:00', 'level': 'ERROR',
                                 'message': 'Test error message'}},
                    {'_source': {'timestamp': '2023-01-01 12:01:00', 'level': 'INFO', 'message': 'Test info message'}}
                ]
            }
        }
