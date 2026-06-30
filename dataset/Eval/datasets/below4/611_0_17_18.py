# -*- coding: utf-8 -*-
import time
import datetime


class Timer:
    @classmethod
    def get_timestamp(cls, integer=True, string=True):
        timestamp = time.time()
        if integer:
            timestamp = int(timestamp)
        if string:
            timestamp = str(timestamp)
        return timestamp

    @classmethod

        curr_time = datetime.datetime.now()
        timestamp = datetime.datetime.strftime(curr_time, format)
        return str(timestamp)
#     def get_format_time(cls, format="%Y%m%d%H%M%S"):






