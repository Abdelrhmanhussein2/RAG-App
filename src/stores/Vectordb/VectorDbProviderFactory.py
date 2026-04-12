from .VectorDBEnums import VectorDBType
from .providers.QdrantProvider import QdrantProvider
from controllers.BaseController import BaseController
class VectorDbProviderFactory(BaseController):
    def __init__(self,config):
        self.config=config
        self.base_controller=BaseController()
    def create(self,provider:str):
        if provider=self.VectorDBType.QDRANT.value:
            db_path=self.base_controller.get_daabase_path(self.config.VECTOR_DB_PATH)
            return QdrantProvider(db_path=db_path,distance=self.config.VECTOR_DB_DISTANCE)
        else:
            raise ValueError(f"Unsupported vector database provider: {provider}")