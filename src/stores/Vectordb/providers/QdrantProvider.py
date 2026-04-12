from ..VectorDBinterface import VectorDBinterface
import logging
from qdrant_client import QdrantClient, models
from ..VectorDBEnums import DistanceMetric

class QdrantProvider(VectorDBinterface):
    def __init__(self, db_path: str, distance: str = None):
        self.db_path = db_path
        self.client = None
        self.logger = logging.getLogger(__name__)
        
        if distance == DistanceMetric.COSINE.value:
            self.distance = models.Distance.COSINE
        elif distance == DistanceMetric.DOT.value:
            self.distance = models.Distance.DOT
        elif distance == DistanceMetric.EUCLIDEAN.value:
            self.distance = models.Distance.EUCLIDEAN
        else:
            self.distance = models.Distance.COSINE

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self):
        return self.client.get_collections()

    def get_collections_info(self, collection_name: str):
        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self, collection_name: str):
        return self.client.delete_collection(collection_name=collection_name)

    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        if do_reset:
            self.delete_collection(collection_name)
        
        if not self.is_collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance
                )
            )
            return True
        return False

    def insert_one(self, collection_name: str, text: str, vector: list, metadata: dict = None, record_id: str = None):
        if not self.is_collection_exists(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist")
            return False
        
        try:
            self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=record_id,
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata or {}
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting record: {e}")
            return False
        return True

    def insert_many(self, collection_name: str, texts: list, vectors: list, metadatas: list = None, record_ids: list = None, batch_size: int = 50):
        if not self.is_collection_exists(collection_name):
            self.logger.error(f"Collection {collection_name} does not exist")
            return False

        if metadatas is None:
            metadatas = [None] * len(texts)

        if record_ids is None:
            record_ids = [None] * len(texts)

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadatas = metadatas[i:batch_end]
            batch_ids = record_ids[i:batch_end]

            records = [
                models.Record(
                    id=batch_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x],
                        "metadata": batch_metadatas[x] or {}
                    }
                )
                for x in range(len(batch_texts))
            ]

            try:
                self.client.upload_records(
                    collection_name=collection_name,
                    records=records
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False
        return True

    def search_vectors(self, collection_name: str, query_vector: list, top_k: int):
        try:
            search_result = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=top_k
            )
            return search_result
        except Exception as e:
            self.logger.error(f"Error while searching: {e}")
            return None
