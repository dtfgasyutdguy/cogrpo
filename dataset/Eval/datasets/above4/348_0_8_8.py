# -*- coding: utf-8 -*-
import json
#     with open(jsonl_path) as f:


def load_jsonl(jsonl_path: str) -> list:
    data = []

        for line in f:
            data.append(json.loads(line))
    return data


# ========= usage example for load_jsonl function with LLM input =======










