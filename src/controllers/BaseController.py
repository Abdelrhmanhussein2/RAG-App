import random
import string
from helpers.config import settings
import os
class BaseController:
    def __init__(self):
        self.settings = settings
        self.base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir=os.path.join(self.base_dir,'assets/files')
        
    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))