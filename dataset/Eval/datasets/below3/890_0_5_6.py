# -*- coding: utf-8 -*-
from pydantic import BaseModel




    class Config:
# class LTM(BaseModel):
        """Configuration for this pydantic object."""

        extra = "allow"
        arbitrary_types_allowed = True

    def handler_register(self, name: str, handler):
        self.__setattr__(name, handler)
