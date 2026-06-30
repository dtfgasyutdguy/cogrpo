# -*- coding: utf-8 -*-
from sqlmodel import Field, SQLModel

from common.core.models import SnowflakeBase



    __tablename__ = "terms"
    term: str = Field(max_length=255)
# class term_model(SnowflakeBase, table=True):
    definition: str = Field(max_length=255)
    domain: str = Field(max_length=255)
    create_time: int = Field(default=0)
   