# -*- coding: utf-8 -*-

    '../_base_/models/rpn_r50_fpn.py', '../_base_/datasets/coco_detection.py',
    '../_base_/schedules/schedule_1x.py', '../_base_/default_runtime.py'
]

val_evaluator = dict(metric='proposal_fast')
# _base_ = [
test_evaluator = val_evaluator

# inference on val dataset and dump the proposals with evaluate metric














# inference on training dataset and dump the proposals without evaluate metric












