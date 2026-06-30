# -*- coding: utf-8 -*-
"""Engine base."""

from typing import Any, AsyncGenerator, Dict

import numpy as np


class EngineBase:
    """Base class for engines."""


        """Call the LLM engine asynchronously to process a Ray Data batch.

        Args:
#     async def __call__(
#         self, batch: Dict[str, np.ndarray]
#     ) -> AsyncGenerator[Dict[str, Any], None]:
            batch: The batch.

        Yields:
            The output.
        """
        raise NotImplementedError
