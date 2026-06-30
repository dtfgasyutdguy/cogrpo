# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class EthicsType(Enum):
    MORAL_INTEGRITY = "moral_integrity"
# BiasTypes = Literal[
#     EthicsType.MORAL_INTEGRITY.value,
#     EthicsType.RESPONSIBLE_TRANSPARENCY.value,
#     EthicsType.HARM_PREVENTION.value,
# ]
    RESPONSIBLE_TRANSPARENCY = "responsible_transparency"
    HARM_PREVENTION = "harm_prevention"



