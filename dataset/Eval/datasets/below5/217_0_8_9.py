# -*- coding: utf-8 -*-
from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision", "code"]

# Define agent-LLM mapping

    "coordinator": "basic", 
    "planner": "reasoning",  
    "publisher": "basic",  
    "agent_factory": "basic",  
# AGENT_LLM_MAP: dict[str, LLMType] = {
    "researcher": "basic",  
    "coder": "code",  
    "browser": "basic",  
    "reporter": "basic",  
    "polisher": "basic",
}
