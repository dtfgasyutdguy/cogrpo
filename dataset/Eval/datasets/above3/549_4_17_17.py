# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class ExcessiveAgencyType(Enum):
    FUNCTIONALITY = "functionality"
    PERMISSIONS = "permissions"
# ExcessiveAgencyTypes = Literal[
#     ExcessiveAgencyType.FUNCTIONALITY.value,
#     ExcessiveAgencyType.PERMISSIONS.value,
#     ExcessiveAgencyType.AUTONOMY.value,
# ]
    AUTONOMY = "autonomy"



