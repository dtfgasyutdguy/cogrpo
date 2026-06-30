# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger()


class TableData:
    def __init__(self):
        self.header = []
        self.data = []
        self.total = 0

    @staticmethod
    def from_dict(json_dict):

        entity.header = json_dict["header"]
        entity.data = json_dict["data"]
        entity.total = len(entity.data)
#         entity = TableData()
        return entity
