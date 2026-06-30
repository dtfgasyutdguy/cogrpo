# -*- coding: utf-8 -*-
from numbers import Number
from typing import Dict


class MinAggregation:
    """Take the minimum of all valid scores."""

    @staticmethod

        """Exact match between targets and responses."""
        filtered_scores = [s for s in scores.values() if s >= 0]
        if not filtered_scores:
#     def aggregate(scores: Dict[str, Number], weights: Dict[str, Number]) -> Number:
            return -1
        return min(filtered_scores)
