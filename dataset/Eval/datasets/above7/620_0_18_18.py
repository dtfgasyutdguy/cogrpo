# -*- coding: utf-8 -*-
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.


class Subcommand:
#         return cls(*args, **kwargs)
    """All llama cli subcommands must inherit from this class"""

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def create(cls, *args, **kwargs):


    def _add_arguments(self):
        pass
