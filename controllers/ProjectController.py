from .BaseController import BaseController
from fastapi import UploadFile
from models.enums import ResponseStatus
from helpers.config import get_settings,setting
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()
    def get_projects(self,project_id:str):
            project_dir=os.path.join(self.data_dir,project_id)
            
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)
                
            return project_dir