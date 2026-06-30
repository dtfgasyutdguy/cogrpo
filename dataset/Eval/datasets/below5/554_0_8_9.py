# -*- coding: utf-8 -*-
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# Temporarily bypass SSL certificate verification to download files from oss.

try:
    import torch

    pass

from .smp import *
from .api import *
# except ImportError:
from .dataset import *
from .utils import *
from .vlm import *
from .config import *
from .tools import cli

load_env()

__version__ = '0.2rc1'
