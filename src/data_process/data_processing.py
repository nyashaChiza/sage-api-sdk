import json
import requests
from loguru import logger
from src.connection import Connection


class Process:
    def __init__(self, connection: Connection) -> None:
        self.session = connection.get_connection()
        self.connection = connection

    def process_header(self, api_header: str):
        url = f"{self.connection.base_url()}api/apibase/process/{api_header}"
        
        try:
            response = self.connection.session.post(url)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

            # Optionally, log the successful response
            logger.info(f"Successfully processed header: {api_header}")
            return response.json()  # Return the JSON response

        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
            return {"success": False, "error": str(http_err)}

        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Connection error occurred: {conn_err}")
            return {"success": False, "error": "Connection error"}

        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Timeout error occurred: {timeout_err}")
            return {"success": False, "error": "Request timed out"}

        except requests.exceptions.RequestException as req_err:
            logger.error(f"An error occurred: {req_err}")
            return {"success": False, "error": str(req_err)}

        except json.JSONDecodeError as json_err:
            logger.error(f"JSON decode error: {json_err} - Response text: {response.text}")
            return {"success": False, "error": "Invalid JSON response"}

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return {"success": False, "error": str(e)}