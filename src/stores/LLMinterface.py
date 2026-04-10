from abc import ABC , abstractmethod

class LLMInterface(ABC):
    
    @abstractmethod
    def set_generation_model(self,model_id:str):
        pass
    
    
    @abstractmethod
    def set_embedding_model(self,model_id:str,embedding_size:int):
        pass
    
    @abstractmethod
    def generate_response(self, prompt:str, chat_history:list[] ,max_tokens:int=1000,temperature:float=None):
        pass
    
    @abstractmethod
    def get_embedding(self, text: str, document_type:str=None):
        pass

    @abstractmethod
    def construct_prompt(self,prompt:str,role:str=None):
        pass