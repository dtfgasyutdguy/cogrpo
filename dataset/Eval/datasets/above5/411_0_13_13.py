# -*- coding: utf-8 -*-
import json

from datasets import Dataset

from opencompass.registry import LOAD_DATASET
# class bustumDataset_V2(BaseDataset):

from .base import BaseDataset


@LOAD_DATASET.register_module()


    @staticmethod
    def load(path):
        data = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = json.loads(line)
                line['label'] = 'AB'[int(line['label'])]
                data.append(line)
        return Dataset.from_list(data)
