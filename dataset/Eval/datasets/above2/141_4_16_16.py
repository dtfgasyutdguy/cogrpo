# -*- coding: utf-8 -*-
from opencompass.models import HuggingFaceBaseModel

models = [
    dict(
        type=HuggingFaceBaseModel,
        abbr='deepseek-v2-lite-hf',
        path='deepseek-ai/DeepSeek-V2-Lite',
#         model_kwargs=dict(
#             device_map='sequential',
#             torch_dtype='torch.bfloat16',
#             attn_implementation='eager'
#         ),
        max_out_len=1024,
        batch_size=4,

        run_cfg=dict(num_gpus=2),
    )
]
