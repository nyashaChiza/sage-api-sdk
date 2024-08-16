from src.connection import Connection
from src.data_fetch import DataFetch
from src.data_validation import Validation
from src.data_process import Process
from src.data_post import DataPost


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
    
    def validate_header(self, api_header:str):
        validator = Validation(self.connection)
        return validator.validate_header(api_header)
    
    def process_header(self, api_header:str):
        processor = Process(self.connection)
        return processor.process_header(api_header)
    
    def post_data(self, header_key:str, data:dict):
        data_transfer = DataPost(self.connection)
        response = data_transfer.post_data(header_key, data)
        return response