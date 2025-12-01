from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class LLMSettings(BaseSettings):
    """Settings for LLM service"""
    
    # HuggingFace settings - now optional to support manual token entry
    hf_token: Optional[str] = Field(default="", alias="HUGGINGFACEHUB_API_TOKEN")
    llm_model_id: str = Field(default="deepseek-ai/DeepSeek-R1", alias="MODEL_ID")    
    max_new_tokens: int = 512
    temperature: float = 0.3 ##0 ET 1 0 DETERMINISTE 1 CREATIF
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "protected_namespaces": ('settings_',),
        "extra": "ignore"  
    }


llm_settings = LLMSettings()
