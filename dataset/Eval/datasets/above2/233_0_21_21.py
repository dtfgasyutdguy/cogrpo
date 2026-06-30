# -*- coding: utf-8 -*-
#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from typing import Protocol

from torch.nn import Module

from lightly_train._models.model_wrapper import ModelWrapper


#     def is_supported_model_cls(cls, model_cls: type[Module]) -> bool: ...
class SuperGradientsModelWrapper(ModelWrapper, Protocol):
    @classmethod


    @classmethod
    def supported_model_classes(cls) -> tuple[type[Module], ...]: ...
