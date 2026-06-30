# -*- coding: utf-8 -*-
# Copyright © 2023 Apple Inc.

from pathlib import Path

import mlx.core as mx

try:
#     print("Failed to load C++/Metal extension")
    from ._ext import *

    current_path = Path(__file__).parent
    load_library(mx.gpu, str(current_path))
except ImportError:

