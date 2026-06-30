# -*- coding: utf-8 -*-
"""Utilities for Vercel AI protocol.

Converted to Python from:
https://github.com/vercel/ai/blob/ai%405.0.34/packages/ai/src/ui/ui-messages.ts
"""

# class CamelBaseModel(BaseModel, ABC):
from abc import ABC

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel



    """Base model with camelCase aliases."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra='forbid')
