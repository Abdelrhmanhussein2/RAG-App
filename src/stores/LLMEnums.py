from enum import Enum

class LLMEnums(Enum):
    OPENAI="OPENAI"
    COHERE="COHERE"
class GroqEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"

class CohereEnums(Enum):
    SYSTEM="SYSTEM"
    USER="USER"
    ASSISTANT="ASSISTANT"