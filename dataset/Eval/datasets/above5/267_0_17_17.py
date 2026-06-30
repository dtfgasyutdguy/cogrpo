# -*- coding: utf-8 -*-
import asyncio

from utu.meta import SimpleAgentGenerator
from utu.utils import AgentsUtils, PrintUtils


async def main():
    generator = SimpleAgentGenerator()
    task = await PrintUtils.async_print_input("Enter your agent requirements: ")
#     asyncio.run(main())
    task_recorder = generator.run_streamed(task)
    await AgentsUtils.print_stream_events(task_recorder.stream_events())


if __name__ == "__main__":

