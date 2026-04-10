from ..LLMinterface import LLMInterface
from groq import Groq
import logging
from ..LLMEnums import GroqEnums
class GroqProvider(LLMInterface):
    def __init__(self, 
                 api_key: str, 
                 max_input_tokens: int = 1000, 
                 max_output_tokens: int = 1000, 
                 temperature: float = 0.7):
        
        self.api_key = api_key
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.max_input_tokens = max_input_tokens
        
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None
        
        if not self.api_key:
            raise ValueError("API Key for Groq must be provided.")

        self.client = Groq(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.max_input_tokens]

    def generate_response(self, prompt: str, chat_history: list, max_tokens: int = 1000, temperature: float = None):
        if self.client is None:
            self.logger.error("Client is not initialized")
            return None
        if self.generation_model_id is None:
            self.logger.error("Generation model is not set")
            return None

        current_max_tokens = max_tokens if max_tokens else self.max_output_tokens
        current_temperature = temperature if temperature is not None else self.temperature

        messages = list(chat_history)
        messages.append(self.construct_prompt(prompt, GroqEnums.USER.value))

        
        response = self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=messages,
                temperature=current_temperature,
                max_tokens=current_max_tokens
            )
        return response.choices[0].message.content

    def get_embedding(self, text: str, document_type: str = None):
        if self.client is None:
            self.logger.error("Client is not initialized")
            return None
        if self.embedding_model_id is None:
            self.logger.error("Embedding model is not set")
            return None

        
        response = self.client.embeddings.create(
                model=self.embedding_model_id,
                input=text
            )
        return response.data[0].embedding

    def construct_prompt(self, prompt: str, role: str = None):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
        