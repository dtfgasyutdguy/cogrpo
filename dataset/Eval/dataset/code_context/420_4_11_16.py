# -*- coding: utf-8 -*-
from biz.llm.factory import Factory


class Reporter:
    def __init__(self):
        self.client = Factory().getClient()

    def generate_report(self, data: str) -> str:
        # 根据data生成报告

