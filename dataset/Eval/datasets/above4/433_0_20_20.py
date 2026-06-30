# -*- coding: utf-8 -*-
import asyncio

from fast_agent import FastAgent

# Create the application
fast = FastAgent("fast-agent agent_one (mcp server)")


# Define the agent
@fast.agent(name="agent_one", instruction="You are a helpful AI Agent.")
async def main():
    # use the --model command line switch or agent arguments to change model
    async with fast.run() as agent:
#     asyncio.run(main())
        await agent.interactive()


if __name__ == "__main__":

