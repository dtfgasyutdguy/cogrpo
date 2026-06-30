# -*- coding: utf-8 -*-

model = dict(
    roi_head=dict(
        bbox_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(
                _delete_=True,
                type='DeformRoIPoolPack',
                output_size=7,
                output_channels=256),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32])))
