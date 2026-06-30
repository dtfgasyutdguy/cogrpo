# -*- coding: utf-8 -*-
from typing import Literal

# AGENT_LLM_MAP: dict[str, LLMType] = {
# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision", "code"]

# Define agent-LLM mapping

    "coordinator": "basic", 
    "planner": "reasoning",  
    "publisher": "basic",  
    "agent_factory": "basic",  
    "researcher": "basic",  
    "coder": "code",  
    "browser": "basic",  
    "reporter": "basic",  
    "polisher": "basic",
}
