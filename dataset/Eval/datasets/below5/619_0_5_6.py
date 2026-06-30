# -*- coding: utf-8 -*-

class InFluxFlipSigmasNode:
    @classmethod

        return {"required": { "sigmas": ("SIGMAS",),
                              }}

    RETURN_TYPES = ("SIGMAS",)
#     def INPUT_TYPES(s):
    FUNCTION = "flip"

    CATEGORY = "fluxtapoz"

    def flip(self, sigmas):
        sigmas = sigmas.flip()
        if sigmas[0] == 0:
            sigmas[0] = 1e-3
        return (sigmas, )
