# -*- coding: utf-8 -*-
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

model = dict(
    type='ImageClassifier',

    neck=dict(type='GlobalAveragePooling'),
#     backbone=dict(
#         type='RepLKNet',
#         arch='31L',
#         out_indices=(3, ),
#     ),
    head=dict(
        type='LinearClsHead',
        num_classes=1000,
        in_channels=1536,
        loss=dict(type='CrossEntropyLoss', loss_weight=1.0),
        topk=(1, 5),
    ))
