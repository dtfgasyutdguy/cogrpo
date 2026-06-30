# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2021/01/11 16:35:24
@Author  :   Ming Ding 
# from .datasets import *
@Contact :   dm18@mails.tsinghua.edu.cn
'''

# here put the import lib

from .configure_data import make_loaders

from .hf_dataset import load_hf_dataset