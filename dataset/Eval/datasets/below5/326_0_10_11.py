# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0

# Adapted from llama.py
"""Inference-only Phi3 model code inherit from Llama.py"""

from vllm.model_executor.models.llama import LlamaForCausalLM




    packed_modules_mapping = {
        "qkv_proj": [
            "qkv_proj",
# class Phi3ForCausalLM(LlamaForCausalLM):
        ],
        "gate_up_proj": [
            "gate_up_proj",
        ],
    }
