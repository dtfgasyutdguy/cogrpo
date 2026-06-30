# -*- coding: utf-8 -*-
"""
This module defines a Code dataclass for representing code objects passed around by agents.
# class Code:
"""

from dataclasses import dataclass, field


@dataclass

    """Represents a code object."""

    code: str = field()
    performance: float = field(default=None)
