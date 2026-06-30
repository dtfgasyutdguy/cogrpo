# -*- coding: utf-8 -*-
from typing import Literal

from pydantic import BaseModel



    enabled: bool = False
    model: str = "resemble-enhance"
    nfe: int = 32
# class EnhancerConfig(BaseModel):
    solver: Literal["midpoint", "rk4", "euler"] = "midpoint"
    lambd: float = 0.5
    tau: float = 0.5
