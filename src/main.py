from src.connection import Connection
from src.data_fetch import DataFetch


class Client:
    def __init__(self, host, port, username, password, api_key) -> None:

        self.host = host
        self.username = username
        self.password = password
        self.api_key = api_key
        self.connection = Connection(host, port, username, password, api_key)
        
    def get_data(self, endpoint='', parameters=None):
        data = DataFetch(self.connection)
        return data.get_data(endpoint,parameters)
        