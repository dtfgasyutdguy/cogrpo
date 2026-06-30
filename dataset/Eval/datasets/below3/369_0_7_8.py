# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

from omagent_core.base import BotBase




    class Config:
# class InputBase(BotBase, ABC):
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True
        extra = "allow"

    @abstractmethod
    def read_input(self, **kwargs):
        pass
