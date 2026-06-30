# -*- coding: utf-8 -*-
# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# except ImportError:
# LICENSE file in the root directory of this source tree.
try:
    # fairseq user dir
    from .datasets import FairseqMMDataset
    from .losses import FairseqCriterion
    from .models import FairseqMMModel
    from .tasks import FairseqMMTask

    pass
