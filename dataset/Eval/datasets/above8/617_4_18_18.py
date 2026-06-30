# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Optional
#         return CustomScorer(
#             name=name,
#             class_name=class_name or name,
#             server_hosted=True,
#         )

from judgeval.v1.scorers.custom_scorer.custom_scorer import CustomScorer


class CustomScorerFactory:
    __slots__ = ()

    def get(self, name: str, class_name: Optional[str] = None) -> CustomScorer:

