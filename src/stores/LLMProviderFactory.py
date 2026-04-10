from .LLMEnums import LLMEnums
from .llm.providers.CohereProvider import CohereProvider
from .llm.providers.GroqProvider import GroqProvider

class LLMProviderFactory:
    def __init__(self,config):
        self.config=config
        
    def get_llm_provider(self, provider: str):
        if provider == LLMEnums.COHERE.value:
            return CohereProvider(
                api_key=self.config.COHERE_API_KEY,
                max_input_tokens=self.config.COHERE_MAX_INPUT_TOKENS,
                max_output_tokens=self.config.COHERE_MAX_OUTPUT_TOKENS,
                temperature=self.config.COHERE_TEMPERATURE
            ) # passing default values    
        elif provider == LLMEnums.GROQ.value:
            return GroqProvider(
                api_key=self.config.GROQ_API_KEY,
                max_input_tokens=self.config.GROQ_MAX_INPUT_TOKENS,
                max_output_tokens=self.config.GROQ_MAX_OUTPUT_TOKENS,
                temperature=self.config.GROQ_TEMPERATURE
            )
        else:   
            raise ValueError(f"Invalid provider: {provider}")