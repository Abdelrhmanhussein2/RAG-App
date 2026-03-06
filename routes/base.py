from fastapi import FastAPI,APIRouter
from helpers.config import get_settings
import os

base_router = APIRouter()
@base_router.get("/")
def welcome():
    app_settings = get_settings()
    
    app_name= app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {"message": f"Welcome to {app_name} version {app_version}!"}