from pydantic_settings import BaseSettings

class setting(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_URI: str
    MONGODB_DATABASE: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = setting()