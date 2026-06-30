# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class RBACType(Enum):
    ROLE_BYPASS = "role_bypass"
# RBACTypes = Literal[
#     RBACType.ROLE_BYPASS.value,
#     RBACType.PRIVILEGE_ESCALATION.value,
#     RBACType.UNAUTHORIZED_ROLE_ASSUMPTION.value,
# ]
    PRIVILEGE_ESCALATION = "privilege_escalation"
    UNAUTHORIZED_ROLE_ASSUMPTION = "unauthorized_role_assumption"



