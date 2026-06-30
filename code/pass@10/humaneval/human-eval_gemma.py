"""
Calculate the pass@10 score of codegemma-1.1-7b-it model a on the HumanEval test set.
"""

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest
from transformers import AutoTokenizer
from typing import List, Dict, Any
import sys
import os
import json
import re
from datasets import load_dataset
import subprocess

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["TORCH_CUDA_ARCH_LIST"] = "8.6"
import torch


torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

IMPORT_HELPER = {
    "python": [
        "import math",
        "import re",
        "import sys",
        "import copy",
        "import datetime",
        "import itertools",
        "import collections",
        "import heapq",
        "import statistics",
        "import functools",
        "import hashlib",
        "import numpy",
        "import numpy as np",
        "import string",
        "from typing import *",
        "from collections import *",
    ],
    "go": [
        "math",
        "strings",
        "fmt",
        "strconv",
        "time",
        "bytes",
        "regexp",
        "sort",
        "math/rand",
        "crypto/md5",
    ],
    "cpp": [
        # "using namespace std;",
        "#include<optional>",
        "#include<cassert>",
        "#include<stdlib.h>",
        "#include<algorithm>",
        "#include<cmath>",
        "#include<math.h>",
        "#include<numeric>",
        "#include<stdio.h>",
        "#include<vector>",
        "#include<set>",
        "#include<map>",
        "#include<queue>",
        "#include<stack>",
        "#include<list>",
        "#include<deque>",
        "#include<boost/any.hpp>",
        "#include<string>",
        "#include<climits>",
        "#include<cstring>",
        "#include<iostream>",
        "#include<sstream>",
        "#include<fstream>",
    ],
    "java": [
        "import java.util.*;",
        "import java.lang.reflect.*;",
        "import org.javatuples.*;",
        "import java.security.*;",
        "import java.math.*;",
        "import java.io.*;",
        "import java.util.stream.*;",
    ],
    "cs": [
        "using System;",
        "using System.Numerics;",
        "using System.Diagnostics;",
        "using System.Collections.Generic;",
        "using System.Linq;",
        "using System.Text;",
        "using System.Security.Cryptography;",
        "using System.Collections.Generic;",
    ],
}


def wrapper(text, job):
    def extract_python_code(text) -> str:
        code_block_pattern = re.compile(rf"```.*?\n(.*?)```", re.DOTALL)
        code_block = code_block_pattern.search(text)
        if code_block is not None:
            return code_block.group(1)
        else:
            return text

    code = extract_python_code(text)
    if "```" in code:
        code = code.replace("```", "")
    func_name = None
    if "name" in job:
        func_name = "_".join(job["name"].split("_")[2:])
    elif "test" in job:
        func_name = re.search(r"assert (.*?)\(.*?\)", job["test"]).group(1)
    if func_name is not None and func_name not in code:
        code = job["prompt"] + code
    code = "\n".join(IMPORT_HELPER["python"]) + "\n" + code

    return code


def get_max_token_length(formatted_prompts, tokenizer):

    max_length = 0
    for prompt in formatted_prompts:
        tokens = tokenizer.encode(prompt, add_special_tokens=True)
        max_length = max(max_length, len(tokens))
    return max_length


def get_humaneval_prompt(doc, language="Python"):
    language = language.lower()
    question = doc["prompt"].strip()
    return """
Please continue to complete the function and return all completed code in a codeblock. Here is the given code to do completion:
```{}
{}
```
""".strip().format(
        language.lower(), question.strip()
    )


def main(NAME: str, MODEL_PATH: str, MAX_LENGTH: int, folder: str = "humaneval"):
    humaneval = load_dataset("openai/openai_humaneval", split="test")
    raw_prompts = [get_humaneval_prompt(sample) for sample in humaneval]
    task_ids = [sample["task_id"] for sample in humaneval]

    sampling_params = SamplingParams(
        n=10,
        temperature=0.8,
        top_p=0.95,
        max_tokens=512,
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

    messages_list = [[{"role": "user", "content": prompt}] for prompt in raw_prompts]
    formatted_prompts: List[str] = tokenizer.apply_chat_template(
        messages_list, tokenize=False, add_generation_prompt=True
    )

    llm = LLM(
        model=MODEL_PATH,
        trust_remote_code=True,
        tensor_parallel_size=1,
        max_model_len=MAX_LENGTH,
        dtype=torch.bfloat16,
        enable_lora=LORA,
        enable_chunked_prefill=not LORA,
        enforce_eager=False,
        gpu_memory_utilization=0.85,
        max_num_seqs=128,
    )

    if LORA:
        SAVE_PATH = f"./grpo_qlora_{NAME}/final_grpo"
        lora_request = None
        if os.path.exists(SAVE_PATH):
            print(f"✅ LoRA adapter found at {SAVE_PATH}.")
            lora_request = LoRARequest(
                lora_name="grpo_lora", lora_int_id=1, lora_path=SAVE_PATH
            )
        else:
            print("⚠️ LoRA not found. Running base model.")
        outputs = llm.generate(
            formatted_prompts, sampling_params, lora_request=lora_request
        )
    else:
        outputs = llm.generate(formatted_prompts, sampling_params)

    all_generations = []
    for output, job in zip(outputs, humaneval):
        completions = []
        for candidate in output.outputs:
            text = candidate.text
            wrapped = wrapper(text, job)
            completions.append(wrapped)
        all_generations.append(completions)

    output_dir = f"./{NAME}/{folder}"
    os.makedirs(output_dir, exist_ok=True)
    samples_path = os.path.join(output_dir, "samples.jsonl")

    with open(samples_path, "w") as f:
        for task_id, completions in zip(task_ids, all_generations):
            for completion in completions:
                json.dump({"task_id": task_id, "completion": completion}, f)
                f.write("\n")

    command = [
        "python",
        "human-eval/human_eval/evaluate_functional_correctness.py",
        samples_path,
        "--k",
        "10",
        "--n_workers",
        str(38),
        "--timeout",
        str(3.0),
    ]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    print(f"📊 {NAME} HumanEval pass@1 & pass@10, Lora={LORA}")
    print(result.stdout.strip())


if __name__ == "__main__":
    NAME = "Qwen2.5-Coder-7B-Instruct"
    LORA = True

    MODEL_PATH = f"LLM_store_path"
    MAX_NEW_TOKENS = 512

    if NAME == "Qwen2.5-Coder-7B-Instruct":
        MAX_LENGTH = MAX_NEW_TOKENS + 448
    elif NAME == "deepseek-coder-6.7b-instruct":
        MAX_LENGTH = MAX_NEW_TOKENS + 503
    elif NAME == "codegemma-1.1-7b-it":
        MAX_LENGTH = MAX_NEW_TOKENS + 444

    print(f"\n🚀 Starting inference for {NAME}...")
    main(NAME, MODEL_PATH, MAX_LENGTH)
    print(f"✅ Completed {NAME}.\n")
