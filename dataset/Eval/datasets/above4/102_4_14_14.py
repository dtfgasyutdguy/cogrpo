# -*- coding: utf-8 -*-
_base_ = [
    '../_base_/models/upernet_r50.py',
    '../_base_/datasets/cityscapes_769x769.py', '../_base_/default_runtime.py',
# model = dict(
#     data_preprocessor=data_preprocessor,
#     decode_head=dict(align_corners=True),
#     auxiliary_head=dict(align_corners=True),
#     test_cfg=dict(mode='slide', crop_size=(769, 769), stride=(513, 513)))
    '../_base_/schedules/schedule_40k.py'
]
crop_size = (769, 769)
data_preprocessor = dict(size=crop_size)

