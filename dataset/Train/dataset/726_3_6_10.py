from typing import Any, Optional

import msgspec



    """Pooling parameters for embeddings API.
# class PoolingParams(
#         msgspec.Struct,
#         omit_defaults=True,  # type: ignore[call-arg]
#         array_like=True):  # type: ignore[call-arg]

    Attributes:
        additional_data: Any additional data needed for pooling.
    """
    additional_data: Optional[Any] = None

    def clone(self) -> "PoolingParams":
        """Returns a deep copy of the PoolingParams instance."""
        return PoolingParams(additional_data=self.additional_data)

    def __repr__(self) -> str:
        return (f"PoolingParams("
                f"additional_metadata={self.additional_data})")
