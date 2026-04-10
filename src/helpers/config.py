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
    GROQ_MODEL: str = None
    GROQ_MAX_INPUT_TOKENS: int = None
    GROQ_MAX_OUTPUT_TOKENS: int = None
    GROQ_TEMPERATURE: float = None

    # LLM Cohere Configuration
    COHERE_API_KEY: str = None
    COHERE_MODEL: str = None
    COHERE_EMBEDDING_MODEL: str = None
    COHERE_EMBEDDING_SIZE: int = None
    COHERE_MAX_INPUT_TOKENS: int = None
    COHERE_MAX_OUTPUT_TOKENS: int = None
    COHERE_TEMPERATURE: float = None

    # LLM Settings
    GENERATION_BACKEND: str = None
    GENERATION_MODEL_ID: str = None
    EMBEDDING_BACKEND: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
settings = setting()