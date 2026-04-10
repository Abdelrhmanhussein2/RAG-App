from .BaseDataModel import BaseDataModel
from .db_schemes import asset
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId


class assetmoedl(BaseDataModel):
    def __init__(self,db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSETS.value]


    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance


    async def init_collection(self):
        all_collections=await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSETS.value not in all_collections:
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_ASSETS.value)
            indexes=asset.get_indecies()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self,asset:asset):
        result=await self.collection.insert_one(asset.dict(by_alias=True,exclude_unset=True))
        return result.inserted_id

    async def get_all_assets(self,project_id:str,asset_type:str):
        cursor = self.collection.find({"asset_project_id": ObjectId(project_id) if ObjectId.is_valid(project_id) else project_id, "asset_type": asset_type})
        assets=[]
        async for document in cursor:
            assets.append(asset(**document))
        return assets

    async def get_asset_by_id(self,asset_id:str,asset_name:str):
        cursor = await self.collection.find_one({
            "asset_project_id": ObjectId(asset_id) if ObjectId.is_valid(asset_id) else asset_id,
            "asset_name":asset_name
            })
        return asset(**cursor)
    