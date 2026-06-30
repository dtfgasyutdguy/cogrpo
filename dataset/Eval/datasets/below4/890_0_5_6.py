# -*- coding: utf-8 -*-
from pydantic import BaseModel




    class Config:
        """Configuration for this pydantic object."""
# class LTM(BaseModel):

        extra = "allow"
        arbitrary_types_allowed = True

    def handler_register(self, name: str, handler):
        self.__setattr__(name, handler)
