# -*- coding: utf-8 -*-
# Minimal initialization for the package
# You might leave this empty, or you could dynamically load modules here 
# but don't execute any logic.

# For example, to dynamically load modules you could:
import os
import importlib
# for filename in os.listdir(module_dir):

module_dir = os.path.dirname(__file__)


    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        importlib.import_module(f'.{module_name}', package=__name__)
