import json
import requests
from loguru import logger
from src.connection import Connection

class DataFetchError(Exception):
    """Custom exception class for DataFetch errors."""
    pass

class DataFetch:
    """Class responsible for fetching data from an endpoint."""

    def __init__(self, connection: Connection) -> None:
    
        self.session = connection.get_connection()
        self.connection = connection

    def get_data(self, endpoint: str, parameters: dict = None) -> dict:
       
        try:
            url = f"{self.connection.base_url}/{endpoint}"
            
            if parameters:
                parameters = {"QueryParameterList": parameters}
                response = self.session.post(url, json=parameters)
            else:
                response = self.session.post(url)
            
            response.raise_for_status() 
            return json.loads(response.content)
        
        except requests.exceptions.RequestException as e:
            logger.error(f'Connection error: {e}')
            raise DataFetchError(f'Error fetching data from {url}: {e}')
