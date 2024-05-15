import json
import pytest
import requests
from src.connection import Connection  

class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"Mock HTTP error: {self.status_code}")

    @property
    def content(self):
        return json.dumps({"access_token": "fake_token"}).encode()

@pytest.fixture
def valid_connection():
    return Connection("example.com", 8080, "username", "password", "api_key")


def test_get_connection_success(valid_connection, monkeypatch):
    # Mock requests.post to return a successful response
    def mock_post(url, *args, **kwargs):
        return MockResponse(200)

    monkeypatch.setattr("requests.Session.post", mock_post)

    connection = valid_connection.get_connection()
    assert isinstance(connection, requests.Session)
    assert connection.headers["Authorization"] == "Bearer fake_token"


def test_get_connection_http_error(valid_connection, monkeypatch):
    # Mock requests.post to raise HTTPError
    def mock_post(url, *args, **kwargs):
        return MockResponse(404)  # or any other non-200 status code

    monkeypatch.setattr("requests.Session.post", mock_post)

    with pytest.raises(ConnectionError):
        valid_connection.get_connection()


def test_get_connection_other_error(valid_connection, monkeypatch):
    # Mock requests.post to raise generic exception
    def mock_post(url, *args, **kwargs):
        raise Exception("Mock other error")

    monkeypatch.setattr("requests.Session.post", mock_post)

    with pytest.raises(ConnectionError):
        valid_connection.get_connection()


def test_test_connection_success(valid_connection, monkeypatch):
    # Mock get_connection to return a valid session
    def mock_get_connection(self):
        return requests.Session()

    monkeypatch.setattr(Connection, "get_connection", mock_get_connection)

    assert valid_connection.test_connection() == {
        "status": True,
        "message": "Connection established successfully"
    }


def test_test_connection_failure(valid_connection, monkeypatch):
    # Mock get_connection to raise ConnectionError
    def mock_get_connection(self):
        raise ConnectionError("Mock connection error")

    monkeypatch.setattr(Connection, "get_connection", mock_get_connection)

    assert valid_connection.test_connection() == {
        "status": False,
        "message": "Mock connection error"
    }
