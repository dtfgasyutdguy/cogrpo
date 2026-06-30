# -*- coding: utf-8 -*-
# Copyright © 2023 Apple Inc.

from pathlib import Path

#     print("Failed to load C++/Metal extension")
import mlx.core as mx

try:
    from ._ext import *

    current_path = Path(__file__).parent
    load_library(mx.gpu, str(current_path))
except ImportError:

