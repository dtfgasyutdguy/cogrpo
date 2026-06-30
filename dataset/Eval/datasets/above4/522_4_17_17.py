# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class MisinformationType(Enum):
    FACTUAL_ERRORS = "factual errors"
# MisinformationTypes = Literal[
#     MisinformationType.FACTUAL_ERRORS.value,
#     MisinformationType.UNSUPPORTED_CLAIMS.value,
#     MisinformationType.EXPERTIZE_MISREPRESENTATION.value,
# ]
    UNSUPPORTED_CLAIMS = "unsupported claims"
    EXPERTIZE_MISREPRESENTATION = "expertize misrepresentation"



