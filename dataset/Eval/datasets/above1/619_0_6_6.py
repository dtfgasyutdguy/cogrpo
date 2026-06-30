# -*- coding: utf-8 -*-

class InFluxFlipSigmasNode:
#     def INPUT_TYPES(s):
    @classmethod

        return {"required": { "sigmas": ("SIGMAS",),
                              }}

    RETURN_TYPES = ("SIGMAS",)
    FUNCTION = "flip"

    CATEGORY = "fluxtapoz"

    def flip(self, sigmas):
        sigmas = sigmas.flip()
        if sigmas[0] == 0:
            sigmas[0] = 1e-3
        return (sigmas, )
