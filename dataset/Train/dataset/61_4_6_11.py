_base_ = '../faster_rcnn/faster-rcnn_r50_fpn_1x_coco.py'
model = dict(
    roi_head=dict(
        bbox_roi_extractor=dict(
            type='SingleRoIExtractor',

            out_channels=256,
            featmap_strides=[4, 8, 16, 32])))
