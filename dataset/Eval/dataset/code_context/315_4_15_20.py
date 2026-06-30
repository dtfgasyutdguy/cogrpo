# -*- coding: utf-8 -*-
"""
Agent which demonstrates Human Input tool
"""

import asyncio

from fast_agent import FastAgent

# Create the application
fast = FastAgent("Human Input")


# Define the agent

async def main() -> None:
    async with fast.run() as agent:
        # this usually causes the LLM to request the Human Input Tool
        await agent("print the next number in the sequence")
        await agent("pretend to be a pizza restaurant and take the users order")
        await agent.interactive(default_prompt="STOP")


if __name__ == "__main__":
    asyncio.run(main())
