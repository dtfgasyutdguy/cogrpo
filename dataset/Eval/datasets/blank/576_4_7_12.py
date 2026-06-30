# -*- coding: utf-8 -*-
_base_ = './faster-rcnn_r50-caffe_c4-1x_coco.py'

train_pipeline = [
    dict(type='LoadImageFromFile', backend_args=_base_.backend_args),
    dict(type='LoadAnnotations', with_bbox=True),

    dict(type='RandomFlip', prob=0.5),
    dict(type='PackDetInputs')
]
_base_.train_dataloader.dataset.pipeline = train_pipeline
