from ..LLMinterface import LLMInterface
from ..LLMEnums import CohereEnums, DocumentTyprEnum
import logging
import cohere
import os

class CohereProvider(LLMInterface):
    def __init__(self,
                 api_key:str,
                 max_input_tokens:int=1000,
                 max_output_tokens:int=1000,
                 temperature:float=0.7):
        
        self.api_key = api_key
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.max_input_tokens = max_input_tokens
        
        self.generation_model_id = None # Will be set via set_generation_model or manually
        self.embedding_model_id = None
        self.embedding_size = None

        if not self.api_key:
            raise ValueError("API Key for Cohere must be provided.")

        self.client = cohere.Client(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)


    def set_generation_model(self,model_id:str):
        self.generation_model_id = model_id
    
    def set_embedding_model(self,model_id:str,embedding_size:int):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size
    
    def process_text(self,text:str):
        return text[:self.max_input_tokens]

    def generate_response(self, prompt:str, chat_history:list,max_tokens:int=1000,temperature:float=None):
        if self.generation_model_id is None:
            raise ValueError("Generation model not set")
        if self.client is None:
            raise ValueError("Client not initialized")
        
        current_max_tokens = max_tokens if max_tokens else self.max_output_tokens
        current_temperature = temperature if temperature is not None else self.temperature

        response = self.client.chat( 
            model=self.generation_model_id,
            message=prompt,
            chat_history=chat_history,
            max_tokens=current_max_tokens,
            temperature=temperature
        )
        if not response.text:
            self.logger.error("Error while generation")
            return None
        return response.text
    
    def get_embedding(self, text: str, document_type:str=None):
        if self.client is None:
            raise ValueError("Client not initialized")
        if self.embedding_model_id is None:
            raise ValueError("Embedding model not set")
        if self.embedding_size is None:
            raise ValueError("Embedding size not set")
        
        input_type=CohereEnums.DOCUMENT
        if document_type==DocumentTyprEnum.QUERY:
            input_type=CohereEnums.QUERY

        response=self.client.embed(
          model= self.embedding_model_id,
          texts=[self.process_text(text)],
          input_type=input_type,

        )
        if not response.embeddings:
            self.logger.error("Embedding not found")
            return None
        return response.embeddings[0]



    def construct_prompt(self,prompt:str,role:str=None):
            return{
                "role":role,
                "text":self.process_text(prompt)
            }
