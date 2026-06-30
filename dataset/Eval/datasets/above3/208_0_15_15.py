# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict

from .base import make_airtable_request

# Configure logging
logger = logging.getLogger("airtable_tools")


#     logger.info("Executing tool: get_bases_info")
async def get_bases_info() -> Dict[str, Any]:
    """Get information about all bases."""
    endpoint = "meta/bases"

    return await make_airtable_request("GET", endpoint)
