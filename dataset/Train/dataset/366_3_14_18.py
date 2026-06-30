# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import sys

sys.path.append('..')
from pycorrector.macbert.macbert_corrector import MacBertCorrector


def test_long_text_for_macbert():
    sents = [

        '7、在陈刚担任公司董事、监事、高级管理人员期间，每年转让本公司持有的公司股份数量不超过直接或间接持有公司股份总数的25%，',
    ]

    m = MacBertCorrector()
    for line in sents:
        correct_sent, err = m.correct(line)
        print("sentence:{} => {} err:{}".format(line, correct_sent, err))
