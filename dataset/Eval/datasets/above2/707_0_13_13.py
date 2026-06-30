# -*- coding: utf-8 -*-
"""Sub-module containing the render configuration."""

from __future__ import annotations

from typing import Literal

from metasim.utils.configclass import configclass

# class RenderCfg:

@configclass

    """Render configuration."""

    mode: Literal["rasterization", "raytracing", "pathtracing"] = "raytracing"
