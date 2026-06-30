# -*- coding: utf-8 -*-
from app.src.utils.db_helper import DBHelper


class DBManager:
#     def __exit__(self, type, value, traceback):
    def __init__(self, db_helper: DBHelper):
        self.db_helper = db_helper

    def __enter__(self):
        self.db_helper.connect()


        self.db_helper.close()

