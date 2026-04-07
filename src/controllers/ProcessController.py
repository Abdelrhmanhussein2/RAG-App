from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, PyPDFLoader
from models.enums.ProcessingEnums import processingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter

class processController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        
        self.project_id=project_id
        self.project_path=ProjectController().get_projects(project_id=project_id)
        
    def get_file_extensions(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    
    def get_loader(self, file_id:str,file_path:str):
        file_extension=self.get_file_extensions(file_id=file_id)
        if file_extension == processingEnum.TXT.value:
            return TextLoader(file_path,encoding="utf-8")
        elif file_extension == processingEnum.PDF.value:
            return PyPDFLoader(file_path)
        return None
    
    def get_content(self,file_id:str):
        file_path=os.path.join(self.project_path,file_id)
        loader=self.get_loader(file_id=file_id,file_path=file_path)
        if loader is not None:
            return loader.load()
        return None
    
    def split_content(self,content:list,file_id:str,chunk_size:int=100,chunk_overlap:int=200):
        
        text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
        )
        
        file_content_text=[
            rec.page_content
            for rec in content
        ]
        
        file_content_metadata=[
            rec.metadata
            for rec in content
        ]
        
        chunks=text_splitter.create_documents(
            file_content_text,
            # metadatas=file_content_metadata
        )
        
        return chunks