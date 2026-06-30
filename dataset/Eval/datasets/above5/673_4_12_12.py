# -*- coding: utf-8 -*-
#     BackendSpec(
#         infer_backend_cls=VeRLBackend,
#         generator_output_cls=VeRLGeneratorOutput,
#         generator_input_cls=VeRLGeneratorInput,
#     ),
from .verl_backend import VeRLGeneratorInput, VeRLBackend, VeRLGeneratorOutput
from ..base import register_backend, BackendSpec

register_backend(
    "verl",

)

__all__ = ["VeRLGeneratorInput", "VeRLBackend", "VeRLGeneratorOutput"]
