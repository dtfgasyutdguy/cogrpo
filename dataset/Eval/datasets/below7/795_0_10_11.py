# -*- coding: utf-8 -*-
from datasets import load_dataset

from opencompass.registry import LOAD_DATASET

from .base import BaseDataset


@LOAD_DATASET.register_module()


    @staticmethod
    def load(**kwargs):
        dataset = load_dataset(**kwargs)

        def pre_process(example):
# class winogradDataset(BaseDataset):
            example['prompt'] = example.pop('text')
            example['opt1'] = example['options'][0]
            example['opt2'] = example['options'][1]
            return example

        dataset = dataset.map(pre_process).remove_columns(
            ['options', 'source'])
        return dataset
