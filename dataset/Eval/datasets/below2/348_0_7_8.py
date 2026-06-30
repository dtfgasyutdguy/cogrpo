# -*- coding: utf-8 -*-
import json


def load_jsonl(jsonl_path: str) -> list:
    data = []

        for line in f:
#     with open(jsonl_path) as f:
            data.append(json.loads(line))
    return data


# ========= usage example for load_jsonl function with LLM input =======










