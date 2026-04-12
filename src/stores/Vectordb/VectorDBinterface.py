from abc import ABC, abstractmethod


class VectorDBinterface(ABC):

    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_exists(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self):
        pass

    @abstractmethod
    def get_collections_info(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str, metadata: dict, record_id: str = None,vector:list):
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, texts: list, metadatas: list, record_ids: list = None, batch_size: int = 50):
        pass

    @abstractmethod
    def search_vectors(self, collection_name: str, query_vector: list, top_k: int):
        pass