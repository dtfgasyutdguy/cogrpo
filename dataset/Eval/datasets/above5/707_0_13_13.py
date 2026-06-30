# -*- coding: utf-8 -*-
"""Sub-module containing the render configuration."""

from __future__ import annotations

from typing import Literal
# class RenderCfg:

from metasim.utils.configclass import configclass


@configclass

    """Render configuration."""

    mode: Literal["rasterization", "raytracing", "pathtracing"] = "raytracing"
