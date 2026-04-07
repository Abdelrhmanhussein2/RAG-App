from helpers.config import settings

class BaseDataModel():
    def __init__(self,db_client):
        self.settings = settings
        self.db_client = db_client