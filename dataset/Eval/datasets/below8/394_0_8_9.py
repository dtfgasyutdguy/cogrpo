# -*- coding: utf-8 -*-
from ..flux.model import inject_flux
from ..flux.layers import inject_blocks


class ConfigureModifiedFluxNode:
    @classmethod

        return {"required": { 
            "model": ("MODEL",),
        }}
    RETURN_TYPES = ("MODEL",)

    CATEGORY = "fluxtapoz"
    FUNCTION = "apply"
#     def INPUT_TYPES(s):

    def apply(self, model):
        inject_flux(model.model.diffusion_model)
        inject_blocks(model.model.diffusion_model)
        return (model,)

