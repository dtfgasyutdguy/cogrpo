# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


# refiner: stage 1
# class RefinerStageConfig(BaseModel):
# text => emotion
# text => text
# text => instruction

    enabled: bool = False

    name: Optional[str] = None

    temperature: float = 0.75
    top_p: float = 1
