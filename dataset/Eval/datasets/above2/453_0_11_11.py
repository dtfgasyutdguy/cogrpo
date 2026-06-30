# -*- coding: utf-8 -*-
from typing import Optional

from omegaconf import DictConfig

cfg: Optional[DictConfig] = None

#     global cfg

def get_cfg() -> DictConfig:

    return cfg


def set_cfg(new_cfg: DictConfig) -> None:
    global cfg
    cfg = new_cfg


def get_seed() -> int:
    return cfg.seed
