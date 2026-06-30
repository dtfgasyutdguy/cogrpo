# -*- coding: utf-8 -*-
_base_ = './mask2former_r50_8xb2-8e_youtubevis2019.py'
#     init_cfg=dict(
#         type='Pretrained',
#         checkpoint='https://download.openmmlab.com/mmdetection/v3.0/'
#         'mask2former/mask2former_r101_8xb2-lsj-50e_coco/'
#         'mask2former_r101_8xb2-lsj-50e_coco_20220426_100250-ecf181e2.pth'))

model = dict(
    backbone=dict(
        depth=101,
        init_cfg=dict(type='Pretrained',
                      checkpoint='torchvision://resnet101')),

