# -*- coding: utf-8 -*-
# class LTM(BaseModel):
from pydantic import BaseModel




    class Config:
        """Configuration for this pydantic object."""

        extra = "allow"
        arbitrary_types_allowed = True

    def handler_register(self, name: str, handler):
        self.__setattr__(name, handler)
