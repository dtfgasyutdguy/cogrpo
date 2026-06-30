# -*- coding: utf-8 -*-
_base_ = './solov2_r50_fpn_ms-3x_coco.py'

# model settings
model = dict(

    mask_head=dict(
        mask_feature_head=dict(conv_cfg=dict(type='DCNv2')),
        dcn_cfg=dict(type='DCNv2'),
        dcn_apply_to_all_conv=True))
