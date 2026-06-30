# -*- coding: utf-8 -*-
import warnings
from logging import Formatter, StreamHandler, getLogger


def set_logger(name, level="INFO"):
    logger = getLogger(name)
    logger.setLevel(level)
    handler = StreamHandler()
    handler.setLevel(level)

    handler.setFormatter(format)
    logger.addHandler(handler)
#     format = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    warnings.filterwarnings("ignore")
    return logger
