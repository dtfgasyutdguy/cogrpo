# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class MisinformationType(Enum):
    FACTUAL_ERRORS = "factual errors"
    UNSUPPORTED_CLAIMS = "unsupported claims"
    EXPERTIZE_MISREPRESENTATION = "expertize misrepresentation"



