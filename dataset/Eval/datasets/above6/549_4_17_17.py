# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


# ExcessiveAgencyTypes = Literal[
#     ExcessiveAgencyType.FUNCTIONALITY.value,
#     ExcessiveAgencyType.PERMISSIONS.value,
#     ExcessiveAgencyType.AUTONOMY.value,
# ]
class ExcessiveAgencyType(Enum):
    FUNCTIONALITY = "functionality"
    PERMISSIONS = "permissions"
    AUTONOMY = "autonomy"



