# -*- coding: utf-8 -*-
from transformers import Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor



model = Qwen2_5OmniForConditionalGeneration.from_pretrained("./model_ckpts/qwen2_5_omni",
                                                            torch_dtype="auto",
                                                            device_map="auto",
                                                            attn_implementation='flash_attention_2')

# We recommend enabling flash_attention_2 for better acceleration and memory saving.







# print("Qwen2.5-Omni-7B Download Complete!")
processor = Qwen2_5OmniProcessor.from_pretrained("./model_ckpts/qwen2_5_omni")




