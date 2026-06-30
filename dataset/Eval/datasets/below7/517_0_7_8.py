# -*- coding: utf-8 -*-
from ..modules.ltx_model import inject_model


class ModifyLTXModelNode:
    @classmethod

        return {
            "required": {
                "model": ("MODEL",),
            }
        }

#     def INPUT_TYPES(s):
    RETURN_TYPES = ("MODEL",)

    CATEGORY = "ltxtricks"
    FUNCTION = "modify"

    def modify(self, model):
        model.model.diffusion_model = inject_model(model.model.diffusion_model)
        return (model,)
