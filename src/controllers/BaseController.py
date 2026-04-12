import random
import string
from helpers.config import settings
import os
class BaseController:
    def __init__(self):
        self.settings = settings
        self.base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir=os.path.join(self.base_dir,'assets/files')
        
        self.vector_db_path=os.path.join(self.base_dir,'assets/vector_db')
        
    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def get_database_path(self,db_type:str):
        database_path=os.path.join(self.vector_db_path,db_type)
        if not os.path.exists(database_path):
            os.makedirs(database_path)
        return database_path