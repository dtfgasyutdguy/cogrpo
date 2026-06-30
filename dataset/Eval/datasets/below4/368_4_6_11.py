# -*- coding: utf-8 -*-
_base_ = './solov2_r50_fpn_ms-3x_coco.py'

# model settings
model = dict(

    mask_head=dict(
        mask_feature_head=dict(conv_cfg=dict(type='DCNv2')),
        dcn_cfg=dict(type='DCNv2'),
#     backbone=dict(
#         depth=101,
#         init_cfg=dict(checkpoint='torchvision://resnet101'),
#         dcn=dict(type='DCNv2', deformable_groups=1, fallback_on_stride=False),
#         stage_with_dcn=(False, True, True, True)),
        dcn_apply_to_all_conv=True))
