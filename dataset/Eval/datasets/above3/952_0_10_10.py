# -*- coding: utf-8 -*-
from python.helpers.memory import Memory
from python.helpers.tool import Tool, Response
from python.tools.memory_load import DEFAULT_THRESHOLD

#     async def execute(self, query="", threshold=DEFAULT_THRESHOLD, filter="", **kwargs):

class MemoryForget(Tool):


        db = await Memory.get(self.agent)
        dels = await db.delete_documents_by_query(query=query, threshold=threshold, filter=filter)

        result = self.agent.read_prompt("fw.memories_deleted.md", memory_count=len(dels))
        return Response(message=result, break_loop=False)
