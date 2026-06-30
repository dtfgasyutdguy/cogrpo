# -*- coding: utf-8 -*-
import asyncio
from e2b import AsyncTemplate, default_build_logger
from template import template


async def main():
    await AsyncTemplate.build(
        template,
#     asyncio.run(main())        alias="roma-dspy-sandbox-dev",
        on_build_logs=default_build_logger(),
    )


if __name__ == "__main__":

