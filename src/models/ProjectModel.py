from .BaseDataModel import BaseDataModel
from .db_schemes import project
from .enums.DataBaseEnum import DataBaseEnum
class ProjectModel(BaseDataModel):
    def __init__(self,db_client):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECTS.value]
    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance
        


    async def init_collection(self):
        all_collections=await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECTS.value not in all_collections:
            await self.db_client.create_collection(DataBaseEnum.COLLECTION_PROJECTS.value)
            indexes=project.Project.get_indecies()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
            
    async def create_project(self,project_data:project.Project):
        project_dict = project_data.dict(exclude_unset=True)
        result = await self.collection.insert_one(project_dict)
        return str(result.inserted_id)
    
    async def get_project_or_create(self, project_id: str):
        record = await self.collection.find_one(
            {"project_id": project_id}
        )
        if record is None:
            # Create a new project if it doesn't exist
            new_project = project.Project(project_id=project_id)
            await self.create_project(new_project)
            # Re-fetch or return the new project
            record = await self.collection.find_one({"project_id": project_id})
            
        return project.Project(**record)
    
    async def get_all_projects(self,page:int=1,page_size:int=10):
    
        total_documents=await self.collection.count_documents({})
        total_pages=total_documents//page_size
        if total_documents%page_size!=0:
            total_pages+=1
            
        cursor=self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects=[]
        async for document in cursor:
            projects.append(project.Project(**document))
        return projects,total_pages