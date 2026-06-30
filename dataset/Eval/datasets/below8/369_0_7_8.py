# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from omagent_core.base import BotBase




    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
        extra = "allow"

# class InputBase(BotBase, ABC):
    @abstractmethod
    def read_input(self, **kwargs):
        pass
