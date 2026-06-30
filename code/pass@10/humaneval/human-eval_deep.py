"""
Calculate the pass@10 score of deepseek-coder-6.7b-instruct model a on the HumanEval test set.
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

import re

languge_settings = {
    "python": {
        "full_name": "Python",
        "indent": 4,
    },
    "cpp": {
        "full_name": "cpp",
        "indent": 0,
        "main": "int main()",
    },
    "java": {
        "full_name": "Java",
        "indent": 4,
        "main": "public static void main",
    },
    "cs": {
        "full_name": "csharp",
        "indent": 0,
        "main": "public static void Main",
    },
    "php": {
        "full_name": "PHP",
        "indent": 0,
    },
    "ts": {
        "full_name": "TypeScript",
        "indent": 0,
    },
    "js": {"full_name": "JavaScript", "indent": 0},
    "sh": {"full_name": "Bash", "indent": 0},
}


def get_function_name(question: str, lang: str):
    func_lines = [x for x in question.strip().split("\n") if x.strip()]

    if lang.lower() == "python":
        func_idx = [
            i for i in range(len(func_lines)) if func_lines[i].startswith("def ")
        ][-1]
        func_name = func_lines[func_idx].split("(")[0].strip()
        func_prefix = "\n".join(func_lines[:func_idx])
        return func_name, func_prefix

    func_name = func_lines[-1].split("{")[0].strip()
    func_prefix = "\n".join(func_lines[:-1])
    return func_name, func_prefix


def extract_generation_code(example: str, lang_code: str, verbose: bool = False):
    task_id = example["task_id"]
    output = example.get("output", example.get("gpt_completion"))
    question = example["prompt"].strip()
    setting = languge_settings[lang_code]
    lang = setting["full_name"]
    indent = setting["indent"]

    try:
        code_block: str = re.findall(
            f"```{lang.lower()}\n(.*?)```", output, re.DOTALL | re.IGNORECASE
        )[0]

        if setting.get("main", None) and setting["main"] in code_block:
            main_start = code_block.index(setting["main"])
            code_block = code_block[:main_start]

        func_name, func_prefix = get_function_name(question, lang)

        try:
            start = code_block.lower().index(func_name.lower())
            indent = 0
            while start - indent >= 0 and code_block[start - indent - 1] == " ":
                indent += 1

            try:
                end = code_block.rindex("\n" + " " * indent + "}")
            except:
                end = len(code_block)
        except:
            start = 0
            try:
                end = code_block.rindex("\n" + " " * indent + "}")
            except:
                end = len(code_block)

        body = code_block[start:end]

        if lang_code.lower() in ["php", "ts", "js"]:
            body += "\n" + " " * indent + "}"

        generation = func_prefix + "\n" + body + "\n"

    except Exception as ex:
        print(
            "Failed to extract code block with error `{}`:\n>>> Task: {}\n>>> Output:\n{}".format(
                ex, task_id, output
            )
        )
        generation = example["prompt"] + "\n" + output

    return generation


def build_deepseekcoder_instruction(languge: str, question: str):
    return """
Please continue to complete the function. You are not allowed to modify the given code and do the completion only. Please return all completed function in a codeblock. Here is the given code to do completion:
```{}
{}
```
""".strip().format(
        languge.lower(), question.strip()
    )


def main(NAME: str, MODEL_PATH: str, MAX_LENGTH: int, folder: str = "humaneval"):
    humaneval = load_dataset("openai/openai_humaneval", split="test")
    raw_prompts = [
        build_deepseekcoder_instruction("Python", sample["prompt"])
        for sample in humaneval
    ]
    task_ids = [sample["task_id"] for sample in humaneval]

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)

    stop_id = tokenizer.convert_tokens_to_ids("<|EOT|>")
    assert isinstance(stop_id, int), "Invalid tokenizer, EOT id not found"

    sampling_params = SamplingParams(
        n=10,
        temperature=0.8,
        top_p=0.95,
        stop_token_ids=[stop_id],
        max_tokens=512,
    )

    if NAME == "starcoder2-7b-instruct":
        formatted_prompts = raw_prompts
    else:
        messages_list = [
            [{"role": "user", "content": prompt}] for prompt in raw_prompts
        ]
        formatted_prompts: List[str] = tokenizer.apply_chat_template(
            messages_list, tokenize=False, add_generation_prompt=True
        )

    llm = LLM(
        model=MODEL_PATH,
        trust_remote_code=True,
        tensor_parallel_size=4,
        max_model_len=MAX_LENGTH,
        dtype=torch.bfloat16,
        enable_lora=LORA,
        enable_chunked_prefill=not LORA,
        enforce_eager=False,
        gpu_memory_utilization=0.85,
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

    all_samples = []

    for i, (ex, output_group) in enumerate(zip(humaneval, outputs)):
        task_id = ex["task_id"]
        prompt = ex["prompt"]

        for j, output in enumerate(output_group.outputs):
            gen_text = output.text

            temp_ex = {"task_id": task_id, "prompt": prompt, "output": gen_text}
            completion = extract_generation_code(temp_ex, "python")
            all_samples.append({"task_id": task_id, "completion": completion})

    output_dir = f"./{NAME}/{folder}"
    os.makedirs(output_dir, exist_ok=True)
    samples_path = os.path.join(output_dir, "samples_pass10.jsonl")

    with open(samples_path, "w") as f:
        for sample in all_samples:
            json.dump(sample, f)
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
    print(f"📊 {NAME} HumanEval pass@10, Lora={LORA}")
    print(result.stdout.strip())


if __name__ == "__main__":
    NAME = "deepseek-coder-6.7b-instruct"
    LORA = True

    MODEL_PATH = f"LLM_store_path"
    MAX_NEW_TOKENS = 512

    if NAME == "Qwen2.5-Coder-7B-Instruct":
        MAX_LENGTH = MAX_NEW_TOKENS + 419
    elif NAME == "deepseek-coder-6.7b-instruct":
        MAX_LENGTH = MAX_NEW_TOKENS + 503
    elif NAME == "codegemma-1.1-7b-it":
        MAX_LENGTH = MAX_NEW_TOKENS + 444

    print(f"\n🚀 Starting inference for {NAME}...")
    main(NAME, MODEL_PATH, MAX_LENGTH)
    print(f"✅ Completed {NAME}.\n")
