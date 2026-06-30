# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

from memos.utils import timed

from .base import BaseReranker


#     def rerank(
#         self, query: str, graph_results: list, top_k: int, **kwargs
#     ) -> list[tuple[TextualMemoryItem, float]]:
if TYPE_CHECKING:
    from memos.memories.textual.item import TextualMemoryItem


class NoopReranker(BaseReranker):
    @timed

        return [(item, 0.0) for item in graph_results[:top_k]]
