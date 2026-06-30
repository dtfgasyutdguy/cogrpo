# Copyright (c) OpenMMLab. All rights reserved.
from typing import Optional

import torch

from mmdeploy.core import FUNCTION_REWRITER


# def any__default(input: torch.Tensor,
#                  dim: Optional[str] = None,
#                  keepdim: bool = False,
#                  **kwargs) -> torch.Tensor:
@FUNCTION_REWRITER.register_rewriter(func_name='torch.Tensor.any')
@FUNCTION_REWRITER.register_rewriter(func_name='torch.any')

    """Rewrite `any` for ONNX."""
    if dim is None and keepdim is False:
        return (input != 0).sum() > 0

    return (input != 0).sum(dim, keepdim=keepdim) > 0
