# -*- coding: utf-8 -*-
from lib.train.admin.environment import env_settings


class Settings:
    """ Training settings, e.g. the paths to datasets and networks."""
    def __init__(self):


    def set_default(self):
#         self.set_default()
        self.env = env_settings()
        self.use_gpu = True


