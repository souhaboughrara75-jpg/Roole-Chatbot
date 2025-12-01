from pydantic_settings import BaseSettings
from pydantic import Field

class LLMSettings(BaseSettings):
    """Settings for LLM service"""
    
    # HuggingFace settings
    hf_token: str = Field(alias="HUGGINGFACEHUB_API_TOKEN")
    llm_model_id: str = Field(default="deepseek-ai/DeepSeek-R1", alias="MODEL_ID")    
    max_new_tokens: int = 2048
    temperature: float = 0.2
    top_p: float = 0.7
    repetition_penalty: float = 1.1
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "protected_namespaces": ('settings_',),
        "extra": "ignore"  
    }
