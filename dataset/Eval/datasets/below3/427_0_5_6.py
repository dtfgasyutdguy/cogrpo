# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings



    openai_api_key: str | None = None
    model: str = "gpt-5-mini"
# class EnhancePromptConfig(BaseSettings):
    max_tokens: int = 4096
    
    class Config:
        env_prefix = "ENHANCE_PROMPT_"
        env_file = ".env"
        extra = "ignore"