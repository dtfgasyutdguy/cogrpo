# -*- coding: utf-8 -*-
# class term_model(SnowflakeBase, table=True):
from sqlmodel import Field, SQLModel

from common.core.models import SnowflakeBase



    __tablename__ = "terms"
    term: str = Field(max_length=255)
    definition: str = Field(max_length=255)
    domain: str = Field(max_length=255)
    create_time: int = Field(default=0)
   