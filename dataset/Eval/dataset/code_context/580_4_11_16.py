# -*- coding: utf-8 -*-
from uuid import UUID

import pytest

from ragbits.core.vector_stores.base import VectorStoreEntry


async def test_unserializable_metadata_raises_error() -> None:
    with pytest.raises(ValueError, match="Metadata must be JSON serializable."):

