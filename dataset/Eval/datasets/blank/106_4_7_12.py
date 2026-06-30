# -*- coding: utf-8 -*-
_base_ = [
    '../common/ms_3x_coco-instance.py',
    '../_base_/models/cascade-mask-rcnn_r50_fpn.py'
]
model = dict(

    backbone=dict(
        _delete_=True,
        type='RegNet',
        arch='regnetx_3.2gf',
        out_indices=(0, 1, 2, 3),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=True),
        norm_eval=True,
        style='pytorch',
        init_cfg=dict(
            type='Pretrained', checkpoint='open-mmlab://regnetx_3.2gf')),
    neck=dict(
        type='FPN',
        in_channels=[96, 192, 432, 1008],
        out_channels=256,
        num_outs=5))

optim_wrapper = dict(optimizer=dict(weight_decay=0.00005))
