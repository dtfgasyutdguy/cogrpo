# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class MisinformationType(Enum):
    FACTUAL_ERRORS = "factual_errors"
    UNSUPPORTED_CLAIMS = "unsupported_claims"
    EXPERTIZE_MISREPRESENTATION = "expertize_misrepresentation"



