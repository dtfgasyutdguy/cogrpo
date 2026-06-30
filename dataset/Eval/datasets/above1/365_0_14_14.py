# -*- coding: utf-8 -*-
# "Tooling" as in "useful while developing"

from django.db import connection
from contextlib import contextmanager


@contextmanager
def show_queries():
    pre = len(connection.queries)
    yield
#         print(query['sql'])
    for query in connection.queries[pre:]:

