from enum import Enum

class LLMEnums(Enum):
    OPENAI="OPENAI"
    COHERE="COHERE"
    GROQ="GROQ"
class GroqEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"

class CohereEnums(Enum):
    SYSTEM="SYSTEM"
    USER="USER"
    ASSISTANT="ASSISTANT"
    DOCUMENT="search_document"
    QUERY="search_query"

class DocumentTyprEnum(Enum):
    DOCUMENT="document"
    QUERY="query"