# -*- coding: utf-8 -*-
_base_ = './mask2former_r50_8xb2-8e_youtubevis2019.py'

model = dict(
    backbone=dict(
        depth=101,
        init_cfg=dict(type='Pretrained',
                      checkpoint='torchvision://resnet101')),

