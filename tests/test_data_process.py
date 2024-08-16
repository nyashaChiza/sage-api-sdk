import pytest
import requests
import json
from unittest.mock import MagicMock, patch
from src.connection import Connection
from src.data_process import Process


class TestProcess:
    @pytest.fixture
    def mock_connection(self):
        # Create a mock connection object
        connection = MagicMock(spec=Connection)
        connection.get_connection.return_value = MagicMock()
        connection.base_url.return_value = "http://example.com/"
        return connection

    @pytest.fixture
    def process(self, mock_connection):
        return Process(mock_connection)

    @patch('src.data_process.logger')
    def test_process_header_success(self, mock_logger, process):
        # Mock the response of the post request
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "value"}
        mock_response.raise_for_status = MagicMock()  # No exception raised
        process.connection.session.post = MagicMock(return_value=mock_response)

        result = process.process_header("test_header")

        assert result == {"data": "value"}
        mock_logger.info.assert_called_once_with("Successfully processed header: test_header")

    @patch('src.data_process.logger')
    def test_process_header_http_error(self, mock_logger, process):
        # Mock the response for HTTP error
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found", response=mock_response)
        process.connection.session.post = MagicMock(return_value=mock_response)

        result = process.process_header("test_header")

        assert result == {"success": False, "error": "Not Found"}
        mock_logger.error.assert_called_once_with("HTTP error occurred: Not Found - Status code: 404")

    @patch('src.data_process.logger')
    def test_process_header_connection_error(self, mock_logger, process):
        # Simulate a connection error
        process.connection.session.post.side_effect = requests.exceptions.ConnectionError("Connection error")

        result = process.process_header("test_header")

        assert result == {"success": False, "error": "Connection error"}
        mock_logger.error.assert_called_once_with("Connection error occurred: Connection error")

    @patch('src.data_process.logger')
    def test_process_header_timeout_error(self, mock_logger, process):
        # Simulate a timeout error
        process.connection.session.post.side_effect = requests.exceptions.Timeout("Timeout error")

        result = process.process_header("test_header")

        assert result == {"success": False, "error": "Request timed out"}
        mock_logger.error.assert_called_once_with("Timeout error occurred: Timeout error")

    @patch('src.data_process.logger')
    def test_process_header_request_exception(self, mock_logger, process):
        # Simulate a general request exception
        process.connection.session.post.side_effect = requests.exceptions.RequestException("Request error")

        result = process.process_header("test_header")

        assert result == {"success": False, "error": "Request error"}
        mock_logger.error.assert_called_once_with("An error occurred: Request error")

    @patch('src.data_process.logger')
    def test_process_header_json_decode_error(self, mock_logger, process):
        # Mock the response for JSON decode error
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()  # No exception raised
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        process.connection.session.post = MagicMock(return_value=mock_response)

        result = process.process_header("test_header")

        assert result == {"success": False, "error": "Invalid JSON response"}
        mock_logger.error.assert_called_once_with("JSON decode error: Expecting value - Response text: <MagicMock name='mock().text' id='...'>")

    @patch('src.data_process.logger')
    def test_process_header_unexpected_error(self, mock_logger, process):
        # Simulate an unexpected error
        process.connection.session.post.side_effect = Exception("Unexpected error")

        result = process.process_header("test_header")

        assert result == {"success": False, "error": "Unexpected error"}
        mock_logger.error.assert_called_once_with("An unexpected error occurred: Unexpected error")