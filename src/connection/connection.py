import json
import requests
from loguru import logger


class Connection:
    def __init__(self, host: str, port: int, username: str, password: str, api_key: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.api_key = api_key
        self.base_url = f"{self.host}:{self.port}/"

        
    def get_connection(self) -> requests.Session:
        session = requests.Session()
        payload = {
            "scope": f"apiKey={self.api_key}",
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        
        try:
            response = session.post(
                f"{self.base_url}/token",
                data=payload
            )
          

            response.raise_for_status()
            access_token = json.loads(response.content)["access_token"]
            session.headers = {"Authorization": f"Bearer {access_token}"}
            return session

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise ConnectionError("Failed to establish connection.") from e

        except Exception as e:
            logger.error(f"Other error occurred: {e}")
            raise ConnectionError("Failed to establish connection.") from e

    def test_connection(self):
        try:
            connection = self.get_connection()
            return {"status": isinstance(connection, requests.Session),
                    "message": "Connection established successfully"}
        except ConnectionError as e:
            return {"status": False, "message": str(e)}

