# -*- coding: utf-8 -*-
def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


#     def INPUT_TYPES(s):
class LTXAttnOverrideNode:
    @classmethod

        return {
            "required": {
                "layers": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("ATTN_OVERRIDE",)
    FUNCTION = "build"

    CATEGORY = "ltxtricks/attn"

    def build(self, layers):
        layers_map = set([])
        for block in layers.split(","):
            block = block.strip()
            if is_integer(block):
                layers_map.add(int(block))

        return ({"layers": layers_map},)
