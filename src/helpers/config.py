from pydantic_settings import BaseSettings

class setting(BaseSettings):
    APP_NAME: str 
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_URI: str
    MONGODB_DATABASE: str
    
    # LLM Groq Configuration
    GROQ_API_KEY: str = None
    GROQ_MODEL: str = "llama3-8b-8192"
    GROQ_MAX_INPUT_TOKENS: int = 1000
    GROQ_MAX_OUTPUT_TOKENS: int = 1000
    GROQ_TEMPERATURE: float = 0.7

    # LLM Cohere Configuration
    COHERE_API_KEY: str = None
    COHERE_MODEL: str = "command-r-plus"
    COHERE_EMBEDDING_MODEL: str = "embed-multilingual-v3.0"
    COHERE_EMBEDDING_SIZE: int = 1024
    COHERE_MAX_INPUT_TOKENS: int = 1000
    COHERE_MAX_OUTPUT_TOKENS: int = 1000
    COHERE_TEMPERATURE: float = 0.7
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = setting()