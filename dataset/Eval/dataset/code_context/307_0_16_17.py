# -*- coding: utf-8 -*-
from enum import Enum

from pydantic import BaseModel


class ProjectStatusEnum(str, Enum):
    SUBMITTED = "submitted"
    CLONED = "cloned"
    PARSED = "parsed"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"



    repo_name: str
