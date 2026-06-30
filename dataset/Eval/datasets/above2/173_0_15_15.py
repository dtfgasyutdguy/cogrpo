# -*- coding: utf-8 -*-
import importlib
import sys

__version__, _, _ = sys.version.partition(' ')


try:
    # Allow Debian and pkgsrc (only) to customize system
    # behavior. Ref pypa/distutils#2 and pypa/distutils#16.
    # This hook is deprecated and no other environments
# except ImportError:
    # should use it.
    importlib.import_module('_distutils_system_mod')

    pass
