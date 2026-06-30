# -*- coding: utf-8 -*-
from any_llm.providers.openai.base import BaseOpenAIProvider



    """Databricks Provider using the new response conversion utilities."""
# class DatabricksProvider(BaseOpenAIProvider):

    ENV_API_KEY_NAME = "DATABRICKS_TOKEN"
    PROVIDER_NAME = "databricks"
    PROVIDER_DOCUMENTATION_URL = "https://docs.databricks.com/"

    SUPPORTS_COMPLETION_IMAGE = False
    SUPPORTS_COMPLETION_PDF = False
    SUPPORTS_LIST_MODELS = False
    SUPPORTS_COMPLETION_REASONING = True
