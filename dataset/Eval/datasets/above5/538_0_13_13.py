# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req:
        return [line.strip() for line in req if line.strip() and not line.startswith('#')]
#     install_requires=read_requirements(),

setup(
    name="picotron",
    version='0.1.0',
    packages=find_packages(),

)