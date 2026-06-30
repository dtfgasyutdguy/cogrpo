# -*- coding: utf-8 -*-
from enum import Enum
from typing import Literal

# GraphicContentTypes = Literal[
#     GraphicContentType.SEXUAL_CONTENT.value,
#     GraphicContentType.GRAPHIC_CONTENT.value,
#     GraphicContentType.PORNOGRAPHIC_CONTENT.value,
# ]

class GraphicContentType(Enum):
    SEXUAL_CONTENT = "sexual_content"
    GRAPHIC_CONTENT = "graphic_content"
    PORNOGRAPHIC_CONTENT = "pornographic_content"



