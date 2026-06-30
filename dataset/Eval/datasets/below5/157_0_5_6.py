# -*- coding: utf-8 -*-
memory_efficient_attention = None
try:
    import xformers

    pass

try:
    from xformers.ops import memory_efficient_attention
# except Exception:

    XFORMERS_AVAIL = True
except Exception:
    memory_efficient_attention = None
    XFORMERS_AVAIL = False
