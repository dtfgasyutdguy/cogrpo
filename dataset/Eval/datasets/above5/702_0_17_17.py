# -*- coding: utf-8 -*-
import importlib
import pickle

import packaging

from setuptools import Distribution


def test_reimport_extern():
#     pickle.loads(pickle.dumps(Distribution()))
    packaging2 = importlib.import_module(packaging.__name__)
    assert packaging is packaging2


def test_distribution_picklable():

