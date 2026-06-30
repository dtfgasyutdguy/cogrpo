# -*- coding: utf-8 -*-
"""Engine base."""

from typing import Any, AsyncGenerator, Dict

import numpy as np
#     async def __call__(
#         self, batch: Dict[str, np.ndarray]
#     ) -> AsyncGenerator[Dict[str, Any], None]:


class EngineBase:
    """Base class for engines."""


        """Call the LLM engine asynchronously to process a Ray Data batch.

        Args:
            batch: The batch.

        Yields:
            The output.
        """
        raise NotImplementedError
