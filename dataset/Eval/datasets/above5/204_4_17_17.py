# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal


class GraphicContentType(Enum):
# GraphicContentTypes = Literal[
#     GraphicContentType.SEXUAL_CONTENT.value,
#     GraphicContentType.GRAPHIC_CONTENT.value,
#     GraphicContentType.PORNOGRAPHIC_CONTENT.value,
# ]
    SEXUAL_CONTENT = "sexual content"
    GRAPHIC_CONTENT = "graphic content"
    PORNOGRAPHIC_CONTENT = "pornographic content"



