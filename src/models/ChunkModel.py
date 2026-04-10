from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne
class ChunkModel(BaseDataModel):
    def __init__(self,db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNKS.value]
    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance


    async def init_collection(self):
        all_collections=await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNKS.value not in all_collections:
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_CHUNKS.value)
            indexes=DataChunk.get_indecies()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )


    async def create_chunk(self,chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict())
        return str(result.inserted_id)


    async def insert_many_chunk(self, chunk: list):
        result = await self.collection.insert_many([c.dict() for c in chunk])
        return [str(id) for id in result.inserted_ids]

    async def get_chunk(self,chunk_id:str):
        chunk=await self.collection.find_one({"_id":chunk_id})
        if chunk is None:
            return None
        return DataChunk(**chunk)

    async def delete_project_chunks(self, project_id: str):
        # تنظيف الـ ID من أي مسافات مخفية
        clean_id = project_id.strip()
        query = {
            "$or": [
                {"chunk_project_id": clean_id},
                {"chunk_project_id": int(clean_id) if clean_id.isdigit() else clean_id},
                {"chunk_project_id": str(clean_id)} # ضمان إضافي
            ]
        }
        print(f"DEBUG - Deleting with query: {query}")
        result = await self.collection.delete_many(query)
        return result.deleted_count