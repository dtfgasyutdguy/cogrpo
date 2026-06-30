# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class MisinformationType(Enum):
# MisinformationTypes = Literal[
#     MisinformationType.FACTUAL_ERRORS.value,
#     MisinformationType.UNSUPPORTED_CLAIMS.value,
#     MisinformationType.EXPERTIZE_MISREPRESENTATION.value,
# ]
    FACTUAL_ERRORS = "factual_errors"
    UNSUPPORTED_CLAIMS = "unsupported_claims"
    EXPERTIZE_MISREPRESENTATION = "expertize_misrepresentation"



