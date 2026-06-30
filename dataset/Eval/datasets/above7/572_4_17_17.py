# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal

# BiasTypes = Literal[
#     EthicsType.MORAL_INTEGRITY.value,
#     EthicsType.RESPONSIBLE_TRANSPARENCY.value,
#     EthicsType.HARM_PREVENTION.value,
# ]

class EthicsType(Enum):
    MORAL_INTEGRITY = "moral_integrity"
    RESPONSIBLE_TRANSPARENCY = "responsible_transparency"
    HARM_PREVENTION = "harm_prevention"



