"""
Calculate the pass@1 score of Qwen2.5-Coder-7B-Instruct model a on the MBPP test set.
"""

from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest
from transformers import AutoTokenizer
from typing import List, Dict, Any
import sys
import os
import json
import re
import traceback
from datasets import load_dataset
import concurrent.futures
import contextlib
from mbpp_eva.evaluation import evaluate_functional_correctness

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["TORCH_CUDA_ARCH_LIST"] = "8.6"
import torch

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

os.environ["TOKENIZERS_PARALLELISM"] = "false"

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
        func_name = re.search(r"assert (.*?)\(.*?\)", job["test_list"][0]).group(1)
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


def format_test_example(q, tests, code: str = None):
    prompt = "{} Your code should pass these tests:\n{}\n".format(
        q.strip(), "\n".join(tests)
    )
    if code:
        code = code.replace("\r", "").replace("\t", "    ")
        prompt += "\n```python\n{}\n```".format(code)
    return prompt


def get_mbpp_prompt(doc, few_shot_prompt):
    q, test, code = doc["text"], doc["test_list"], doc["code"]
    prompt = format_test_example(q, test, code=None)
    prompt_with_shots = """
Please refer the given examples and generate a python function for my problem.
Examples are listed as follows:
{}

Here is my problem:
{}
""".strip().format(
        "\n\n".join(few_shot_prompt), prompt
    )
    return prompt_with_shots


def main(NAME: str, MODEL_PATH: str, MAX_LENGTH: int, folder: str = "mbpp"):
    mbpp = load_dataset("MBPP", split="test")

    examples = [json.loads(x) for x in open("./mbpp_eva/mbpp.jsonl")]
    few_shots = examples[1:4]

    def get_few_shot_example():
        examples_str = []
        for i, obj in enumerate(few_shots):
            q, test, code = obj["text"], obj["test_list"], obj["code"]
            ex_prompt = format_test_example(q, test, code)
            example_prompt = "- Example {}:\n{}".format(i + 1, ex_prompt)
            examples_str += [example_prompt]
        return examples_str

    few_shot_prompt = get_few_shot_example()

    raw_prompts = []

    for ex in mbpp:
        prompt_with_shots = get_mbpp_prompt(ex, few_shot_prompt)

        raw_prompts.append(prompt_with_shots)

    task_ids = [sample["task_id"] for sample in mbpp]
    test_lists = [sample["test_list"] for sample in mbpp]

    sampling_params = SamplingParams(
        temperature=0,
        top_k=1,
        top_p=1.0,
        seed=42,
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
        dtype="auto",
        enable_lora=LORA,
        enable_chunked_prefill=not LORA,
        enforce_eager=False,
    )

    if LORA:
        SAVE_PATH = f"./grpo_qlora_{NAME}/final_grpo"
        lora_request = None
        if os.path.exists(SAVE_PATH):
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

    generated_texts = [output.outputs[0].text for output in outputs]
    full_generations = []
    for text, job in zip(generated_texts, mbpp):
        full_generations.append(wrapper(text, job))

    output_dir = f"./{NAME}/{folder}"
    os.makedirs(output_dir, exist_ok=True)
    samples_path = os.path.join(output_dir, "samples.jsonl")

    samples_for_eval = []
    with open(samples_path, "w") as f:
        for task_id, prompt, completion, test_list in zip(
            task_ids, raw_prompts, full_generations, test_lists
        ):
            record = {
                "prompt": prompt,
                "task_id": task_id,
                "generation": completion,
                "test_list": test_list,
            }
            samples_for_eval.append(record)
            json.dump(record, f)
            f.write("\n")

    result = evaluate_functional_correctness(
        input_file=samples_path,
        tmp_dir="./temps",
        problem_file=os.path.join("./mbpp_eva", f"mbpp_test.jsonl"),
        language="python",
        is_mbpp=True,
    )


if __name__ == "__main__":
    NAME = ""
    LORA = True

    MODEL_PATH = f"LLM_store_path"
    MAX_NEW_TOKENS = 512

    MAX_LENGTH = MAX_NEW_TOKENS + 4282

    print(f"\n🚀 Starting MBPP inference for {NAME}...")
    main(NAME, MODEL_PATH, MAX_LENGTH)
    print(f"✅ Completed {NAME}.\n")
