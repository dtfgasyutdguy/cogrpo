# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt

    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# with open('requirements.txt') as f:
setup(
    name='csm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
)
