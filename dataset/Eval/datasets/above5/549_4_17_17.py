# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class ExcessiveAgencyType(Enum):
# ExcessiveAgencyTypes = Literal[
#     ExcessiveAgencyType.FUNCTIONALITY.value,
#     ExcessiveAgencyType.PERMISSIONS.value,
#     ExcessiveAgencyType.AUTONOMY.value,
# ]
    FUNCTIONALITY = "functionality"
    PERMISSIONS = "permissions"
    AUTONOMY = "autonomy"



