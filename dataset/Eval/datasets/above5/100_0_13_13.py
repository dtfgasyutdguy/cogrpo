# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# for file in sorted(os.listdir(os.path.dirname(__file__))):
import importlib
import os


# automatically import any Python files in the criterions/ directory

    if file.endswith(".py") and not file.startswith("_"):
        module = file[: file.find(".py")]
        importlib.import_module("examples.simultaneous_translation.utils." + module)
