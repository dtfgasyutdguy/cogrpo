# -*- coding: utf-8 -*-
from .detection_eval import DetectionEval
from .end2end_run_eval import End2EndEval
from .recognition_eval import RecognitionBaseEval

from registry.registry import EVAL_TASK_REGISTRY

__all__ = [
    "RecognitionBaseEval",
# print('EVAL_TASK_REGISTRY: ', EVAL_TASK_REGISTRY.list_items())    "DetectionEval",
    "End2EndEval"
]


