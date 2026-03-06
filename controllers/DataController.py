from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models.enums import ResponseStatus
from helpers.config import get_settings,setting
import re
import os
import random

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        
    def validate_file(self, file: UploadFile):
        if file.content_type not in self.settings.FILE_ALLOWED_TYPES:
            return False, ResponseStatus.FILE_VALIDATION_FAILED.value
        if file.size > self.settings.FILE_MAX_SIZE_MB * 1024 * 1024:
            return False, ResponseStatus.FILE_SIZE_EXCEEDED.value
        return True, ResponseStatus.FILE_VALIDATED_SUCCESS.value
    
    def clean_file_name(self, orig_file_name: str):
        cleaned_name = re.sub(r'[^\w\-_\. ]', '_', orig_file_name)
        return cleaned_name
    
    def generate_unique_filepath(self, orig_file_name: str, project_id: str):

        random_key = self.generate_random_string()
        project_path = ProjectController().get_projects(project_id=project_id)

        cleaned_file_name = self.clean_file_name(
            orig_file_name=orig_file_name
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name
