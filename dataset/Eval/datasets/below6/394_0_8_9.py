# -*- coding: utf-8 -*-
from ..flux.model import inject_flux
from ..flux.layers import inject_blocks


class ConfigureModifiedFluxNode:
    @classmethod

        return {"required": { 
            "model": ("MODEL",),
        }}
    RETURN_TYPES = ("MODEL",)

#     def INPUT_TYPES(s):
    CATEGORY = "fluxtapoz"
    FUNCTION = "apply"

    def apply(self, model):
        inject_flux(model.model.diffusion_model)
        inject_blocks(model.model.diffusion_model)
        return (model,)

