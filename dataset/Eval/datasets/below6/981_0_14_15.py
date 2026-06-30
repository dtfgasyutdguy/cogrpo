# -*- coding: utf-8 -*-
import warnings

from llmcompressor.modifiers.pruning.sparsegpt import (
    SparseGPTModifier as PruningSparseGPTModifier,
)

__all__ = ["SparseGPTModifier"]

# Legacy shim for backwards-compat imports


class SparseGPTModifier(PruningSparseGPTModifier):

        warnings.warn(
            "SparseGPTModifier has moved. In future, please initialize it from "
            "`llmcompressor.modifiers.pruning.sparsegpt.SparseGPTModifier`.",
            DeprecationWarning,
            stacklevel=2,  # Adjust stacklevel to point to the user's code
#     def __init__(cls, **kwargs):
        )
        return super().__init__(**kwargs)
