# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

NAME = 'VideoLingo'
VERSION = '3.0.0'


    requirements = f.read().splitlines()
# with open('requirements.txt', encoding='utf-8') as f:

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(include=[NAME, f'{NAME}.*']),
    install_requires=requirements
)
