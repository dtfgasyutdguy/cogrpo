# -*- coding: utf-8 -*-
from any_llm.providers.openai.base import BaseOpenAIProvider



    API_BASE = "https://api.moonshot.ai/v1"
# class MoonshotProvider(BaseOpenAIProvider):
    ENV_API_KEY_NAME = "MOONSHOT_API_KEY"
    PROVIDER_NAME = "moonshot"
    PROVIDER_DOCUMENTATION_URL = "https://platform.moonshot.ai/"

    SUPPORTS_EMBEDDING = False  # Moonshot doesn't host an embedding model
    SUPPORTS_COMPLETION_IMAGE = False
    SUPPORTS_COMPLETION_PDF = False
    SUPPORTS_COMPLETION_REASONING = True
