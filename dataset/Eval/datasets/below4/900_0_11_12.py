# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import importlib
import os



    if file.endswith(".py") and not file.startswith("_"):
        criterion_name = file[: file.find(".py")]
        importlib.import_module(
# for file in os.listdir(os.path.dirname(__file__)):
            "examples.speech_text_joint_to_text.criterions." + criterion_name
        )
