from fastapi import FastAPI
from routes.base import base_router
from routes.data import data_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import settings
from stores.LLMProviderFactory import LLMProviderFactory

app = FastAPI()

@app.middleware("http")
async def normalize_path_middleware(request, call_next):
    path = request.url.path
    if "//" in path:
        # Normalize double slashes
        new_path = path.replace("//", "/")
        # We modify the request scope to the normalized path
        request.scope["path"] = new_path
        
    response = await call_next(request)
    return response

@app.on_event("startup")
async def startup_db_client():
    # settings = settings
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URI)
    app.mongodb = app.mongodb_client[settings.MONGODB_DATABASE]
    app.llm_provider_factory = LLMProviderFactory.create_provider(settings) 
    
    app.generation_provider = app.llm_provider_factory.get_llm_provider(settings.DEFAULT_PROVIDER)
    app.generation_provider.set_generation_model(settings.DEFAULT_GENERATION_MODEL)
    
    app.embedding_provider = app.llm_provider_factory.get_llm_provider(settings.DEFAULT_PROVIDER)
    app.embedding_provider.set_embedding_model(settings.DEFAULT_EMBEDDING_MODEL,settings.DEFAULT_EMBEDDING_SIZE)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()  
    
    
app.include_router(base_router)
app.include_router(data_router)