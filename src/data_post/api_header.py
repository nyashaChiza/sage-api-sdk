import json
import requests
from loguru import logger
from src.connection import Connection


class ApiHeader:
    def __init__(self, connection: Connection) -> None:
        self.session = connection.get_connection()
        self.connection = connection
        
    def get_header(self, header_key:str):
        url = f"{self.connection.base_url()}api/apibase/process/{header_key}"
        response = self.connection.session.post(url)
        return response
        