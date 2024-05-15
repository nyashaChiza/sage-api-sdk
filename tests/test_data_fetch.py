import pytest
import requests
from unittest.mock import MagicMock
from src.connection import Connection
from src.data_fetch import DataFetch, DataFetchError

class MockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")

@pytest.fixture
def connection_mock():
    connection_mock = MagicMock(spec=Connection, base_url='http://example.com')
    session_mock = MagicMock(spec=requests.Session)
    connection_mock.get_connection.return_value = session_mock
    return connection_mock

def test_get_data_connection_error(connection_mock):
    session_mock = connection_mock.get_connection.return_value
    session_mock.post.side_effect = requests.exceptions.ConnectionError("Mock connection error")

    data_fetch = DataFetch(connection_mock)
    with pytest.raises(DataFetchError):
        data_fetch.get_data('endpoint')

def test_get_data_http_error(connection_mock):
    session_mock = connection_mock.get_connection.return_value
    session_mock.post.return_value = MockResponse(404, b'Not Found')

    data_fetch = DataFetch(connection_mock)
    with pytest.raises(DataFetchError):
        data_fetch.get_data('endpoint')
