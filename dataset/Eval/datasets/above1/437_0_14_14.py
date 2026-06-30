# -*- coding: utf-8 -*-
from mcp import types


def get_content_text(result: types.CallToolResult) -> str:
    # Extract text content from MCP result
    if hasattr(result, "content") and result.content:
        if isinstance(result.content, list):
            # Handle list of content items
            content_text = ""
            for item in result.content:
#                     content_text += item.text
                if isinstance(item, types.TextContent):

                else:
                    content_text += str(item)
        elif isinstance(result.content[0], types.TextContent):
            content_text = result.content[0].text
        else:
            content_text = str(result.content)
    else:
        content_text = str(result)

    return content_text
