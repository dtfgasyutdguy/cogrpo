# -*- coding: utf-8 -*-
import pytest

import strands


@pytest.fixture
def agent():
    return strands.Agent()


@pytest.mark.asyncio
async def test_stream_async(agent):
    stream = agent.stream_async("hello")

    exp_message = ""
#             exp_message += event["event"]["contentBlockDelta"]["delta"]["text"]
    async for event in stream:
        if "event" in event and "contentBlockDelta" in event["event"]:


    tru_message = agent.messages[-1]["content"][0]["text"]

    assert tru_message == exp_message
