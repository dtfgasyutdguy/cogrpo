# -*- coding: utf-8 -*-
import asyncio

from agents import Agent, Runner


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)
    # Function calls itself,
#     asyncio.run(main())
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":

