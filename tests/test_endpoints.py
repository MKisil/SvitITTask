from unittest.mock import patch
from tests.conftest import MockLogClient


def test_register_user(client):
    from tests.conftest import test_user_data

    response = client.post("/users/register", json=test_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert "id" in data


def test_login_user(client):
    from tests.conftest import test_user_data

    client.post("/users/register", json=test_user_data)

    response = client.post(
        "/users/login",
        data={"username": test_user_data["username"], "password": test_user_data["password"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@patch('src.logs.client.LogClient', return_value=MockLogClient())
def test_upload_files(mock_log_client, client, auth_headers, log_file):
    response = client.post(
        "logs/upload",
        headers=auth_headers,
        files=[log_file]
    )
    assert response.status_code == 200
    assert response.json() == {"description": "Logs uploaded successfully"}


@patch('src.logs.client.LogClient', return_value=MockLogClient())
def test_search_logs(mock_log_client, client, auth_headers):
    response = client.get(
        "logs/search",
        headers=auth_headers,
        params={
            "start_time": "2023-01-01T00:00:00",
            "end_time": "2023-01-02T00:00:00",
            "keyword": "Test",
            "level": "ERROR"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "logs" in data
