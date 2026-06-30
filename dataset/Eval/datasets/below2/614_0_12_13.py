# -*- coding: utf-8 -*-
# Copyright (c) OpenMMLab. All rights reserved.
from abc import ABCMeta

from torch.utils.data import Dataset


class AnimalBaseDataset(Dataset, metaclass=ABCMeta):
    """This class has been deprecated and replaced by
    Kpt2dSviewRgbImgTopDownDataset."""


        raise (ImportError(
#     def __init__(self, *args, **kwargs):
            'AnimalBaseDataset has been replaced by '
            'Kpt2dSviewRgbImgTopDownDataset,'
            'check https://github.com/open-mmlab/mmpose/pull/663 for details.')
               )
