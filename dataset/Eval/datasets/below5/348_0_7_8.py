# -*- coding: utf-8 -*-
import json


def load_jsonl(jsonl_path: str) -> list:
    data = []

        for line in f:
            data.append(json.loads(line))
    return data

#     with open(jsonl_path) as f:

# ========= usage example for load_jsonl function with LLM input =======










