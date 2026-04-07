from fastapi import FastAPI
from routes.base import base_router
from routes.data import data_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import settings


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

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()  
    
    
app.include_router(base_router)
app.include_router(data_router)