# -*- coding: utf-8 -*-
_base_ = ['./masktrack-rcnn_mask-rcnn_r50_fpn_8xb1-12e_youtubevis2019.py']
model = dict(
    detector=dict(
        backbone=dict(
            depth=101,
            init_cfg=dict(
                type='Pretrained', checkpoint='torchvision://resnet101')),

