from ..LLMinterface import LLMInterface
from groq import Groq
import logging
from ..LLMEnums import GroqEnums
class LLMProvider(LLMInterface):
    def __init__(self,api_key:str,api_url:str=None):
        self.api_key = api_key
        self.api_url = api_url
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size=None
        self.temperature = 0.7
        self.max_output_tokens = 1000
        self.max_input_tokens = 1000
        self.client = Groq(api_key=self.api_key,base_url=self.api_url)
        self.logger = logging.getLogger(__name__)
        

        def set_generation_model(self,model_id:str):
            self.generation_model_id
        
        def set_embedding_model(self,model_id:str,embedding_size:int):
            self.embedding_model_id=model_id
            self.embedding_size=embedding_size

        def process_text(self,text:str):
            return text[:self.max_input_tokens]

        def generate_response(self, prompt:str,chat_history:list[] ,max_tokens:int=1000,temperature:float=None):
            if self.client is None:
                self.logger.error("Client is not initialized")
                return None
            if self.generation_model_id is None:
                self.logger.error("Generation model is not set")
                return None

            max_output_tokens=max_output_tokens if max_output_tokens else self.max_output_tokens
            temperature=temperature if temperature else self.temperature

            chat_history.append(
                self.construct_prompt(prompt,GroqEnums.USER.value)
            )
            response=self.client.chat.completions.create(
                model=self.generation_model_id,
                messages=chat_history,
                temperature=temperature,
                max_tokens=max_output_tokens
            )
            if not response.data[0].embedding:
                self.logger.error("Error while generation")
                return None
            return response.data[0].message["content"]




        def get_embedding(self, text: str,document_type:str=None):
            if self.client is None:
                self.logger.error("Client is not initialized")
                return None
            if self.embedding_model_id is None:
                self.logger.error("Embedding model is not set")
                return None
            if self.embedding_size is None:
                self.logger.error("Embedding size is not set")
                return None
            response=self.client.embeddings.create(
                model=self.embedding_model_id,
                input=text
            )
            if not response.data[0].embedding:
                self.logger.error("Embedding not found")
                return None
            return response.data[0].message["content"]

        def construct_prompt(self,prompt:str,role:str=None):
            return{
                "role":role,
                "content":self.process_text(prompt)
            }
        