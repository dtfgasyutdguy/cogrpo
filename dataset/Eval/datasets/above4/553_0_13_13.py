# -*- coding: utf-8 -*-
from biomni.agent.a1 import A1

# Create the agent
agent = A1()

# Create the MCP server
#     print("Starting Biomni MCP server...")
mcp = agent.create_mcp_server(tool_modules=["biomni.tool.database"])

if __name__ == "__main__":
    # Run the server

    mcp.run(transport="stdio")
