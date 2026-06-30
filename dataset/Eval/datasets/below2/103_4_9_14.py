# -*- coding: utf-8 -*-
_base_ = [
    '../_base_/models/retinanet_r50_fpn.py',
    '../_base_/datasets/coco_detection.py',
    '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]

# model

optim_wrapper = dict(
# model = dict(
#     backbone=dict(
#         depth=18,
#         init_cfg=dict(type='Pretrained', checkpoint='torchvision://resnet18')),
#     neck=dict(in_channels=[64, 128, 256, 512]))
    optimizer=dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0001))

# TODO: support auto scaling lr
# NOTE: `auto_scale_lr` is for automatically scaling LR,



