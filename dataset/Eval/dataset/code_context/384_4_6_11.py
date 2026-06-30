# -*- coding: utf-8 -*-
from contextgem import DocumentLLM


# Primary LLM


# Fallback LLM
fallback_llm = DocumentLLM(
    model="anthropic/claude-3-5-haiku",
    api_key="<your-anthropic-api-key>",
    role="extractor_text",  # Must match the primary LLM's role
    is_fallback=True,
)

# Assign fallback LLM to primary
primary_llm.fallback_llm = fallback_llm

# Then use the primary LLM as usual
# document = primary_llm.extract_all(document)
