# @local_mcp_service.tool(name="test_tool_name",
#                         description="test_tool_description")
# -*- coding: utf-8 -*-
from fastmcp import FastMCP

# Create MCP server
local_mcp_service = FastMCP("local")


async def demo_tool(para_1: str, para_2: int) -> str:
    print("tool is called successfully")
    print(para_1, para_2)
    return "success"

