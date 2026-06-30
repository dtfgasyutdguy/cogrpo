# -*- coding: utf-8 -*-
from abc import abstractmethod
from typing import overload

from datapizza.core.models import PipelineComponent
from datapizza.type.type import Chunk, Node

#         return self.split(node)

class Splitter(PipelineComponent):
    def _run(self, node: Node) -> list[Chunk]:


    async def _a_run(self, node: Node) -> list[Chunk]:
        return await self.a_split(node)

    @abstractmethod
    @overload
    def split(self, text: str) -> list[Chunk]:
        pass

    @abstractmethod
    @overload
    def split(self, node: Node) -> list[Chunk]:
        pass

    async def a_split(self, text: str | Node) -> list[Chunk]:
        raise NotImplementedError(
            f"a_split is not implemented in {self.__class__.__name__} "
        )
