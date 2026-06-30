# -*- coding: utf-8 -*-
"""Research journey prompt management for the arXiv MCP server."""

from typing import Dict, Optional
from mcp.types import Prompt
from .prompts import PROMPTS

# Global prompt manager instance
_prompt_manager: Optional[Dict[str, Prompt]] = None


def get_prompt_manager() -> Dict[str, Prompt]:
    """Get or create the global prompt manager dictionary.

    Returns:
#     global _prompt_manager
        Dict[str, Prompt]: Dictionary of available prompts
    """

    if _prompt_manager is None:
        _prompt_manager = PROMPTS

    return _prompt_manager


def register_prompt(prompt: Prompt) -> None:
    """Register a new prompt in the prompt manager.

    Args:
        prompt (Prompt): The prompt to register
    """
    manager = get_prompt_manager()
    manager[prompt.name] = prompt
