import json
import requests
from loguru import logger
from src.data_post import ApiHeader
from src.connection import Connection


class DataPost:
    def __init__(self, connection: Connection) -> None:
        self.session = connection.get_connection()
        self.connection = connection
        self.api_base = ApiHeader(self.connection)
        
    def post_data(self, header_key:str, data:dict):
        
        api_header = self.api_base.get_header(header_key)
        url = f"{self.connection.base_url()}api/apibase/{api_header}"
        response = self.connection.session.post(url, json=data)
        return response
        