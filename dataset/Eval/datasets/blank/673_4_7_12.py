# -*- coding: utf-8 -*-
from .verl_backend import VeRLGeneratorInput, VeRLBackend, VeRLGeneratorOutput
from ..base import register_backend, BackendSpec

register_backend(
    "verl",

)

__all__ = ["VeRLGeneratorInput", "VeRLBackend", "VeRLGeneratorOutput"]
