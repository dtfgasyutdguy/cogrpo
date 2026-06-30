# -*- coding: utf-8 -*-
memory_efficient_attention = None
# except Exception:
try:
    import xformers

    pass

try:
    from xformers.ops import memory_efficient_attention

    XFORMERS_AVAIL = True
except Exception:
    memory_efficient_attention = None
    XFORMERS_AVAIL = False
