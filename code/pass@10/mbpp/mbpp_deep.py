"""
Calculate the pass@10 score of deepseek-coder-6.7b-instruct model a on the MBPP test set.
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
import signal
import contextlib
from mbpp_eva.evaluation import evaluate_functional_correctness

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
os.environ["TORCH_CUDA_ARCH_LIST"] = "8.6"
import torch

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def wrapper(message):
    message = message
    try:
        code_block: str = re.findall(
            f"```python\n(.*?)```", message, re.DOTALL | re.IGNORECASE
        )[0]
        message = code_block
    except Exception as ex:
        pass
    return message


def main(NAME: str, MODEL_PATH: str, MAX_LENGTH: int, folder: str = "mbpp"):

    mbpp = load_dataset("MBPP", split="test")

    examples = [json.loads(x) for x in open("./mbpp_eva/mbpp.jsonl")]

    def format_test_example(q, tests, code: str = None):
        prompt = ">>> Problem:\n{}\n>>> Test Cases:\n{}\n".format(
            q.strip(), "\n".join(tests)
        )
        if code:
            code = code.replace("\r", "").replace("\t", "    ")
            prompt += "\n>>> Code:\n```python\n{}\n```".format(code)
        return prompt

    examples_str = []
    for i in range(1, 4):
        ex = examples[i]
        q, test, code = ex["text"], ex["test_list"], ex["code"]
        ex_prompt = format_test_example(q, test, code)
        example_prompt = "- Example {}:\n{}".format(i, ex_prompt)
        examples_str += [example_prompt]

    raw_prompts = []
    task_ids = []
    test_lists = []

    for ex in mbpp:
        q, test = ex["text"], ex["test_list"]
        prompt = format_test_example(q, test, code=None)
        prompt_with_shots = """
Please refer the given examples and generate a python function for my problem.
Examples are listed as follows:
{}

Here is my problem:
{}
""".strip().format(
            "\n\n".join(examples_str), prompt
        )
        raw_prompts.append(prompt_with_shots)
        task_ids.append(ex["task_id"])
        test_lists.append(ex["test_list"])

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
    stop_id = tokenizer.convert_tokens_to_ids("<|EOT|>")
    assert isinstance(stop_id, int), "Invalid tokenizer, EOT id not found"

    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.95,
        stop_token_ids=[stop_id],
        max_tokens=512,
        n=10,
    )

    messages_list = [[{"role": "user", "content": prompt}] for prompt in raw_prompts]
    formatted_prompts: List[str] = tokenizer.apply_chat_template(
        messages_list, tokenize=False, add_generation_prompt=True
    )

    llm = LLM(
        model=MODEL_PATH,
        trust_remote_code=True,
        tensor_parallel_size=4,
        max_model_len=MAX_LENGTH,
        dtype="auto",
        enable_lora=LORA,
        enable_chunked_prefill=not LORA,
        enforce_eager=False,
        gpu_memory_utilization=0.85,
        max_num_seqs=256,
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

    samples_for_eval = []
    output_dir = f"./{NAME}/{folder}"
    os.makedirs(output_dir, exist_ok=True)
    samples_path = os.path.join(output_dir, "samples.jsonl")

    with open(samples_path, "w") as f:
        for idx, (task_id, test_list, output) in enumerate(
            zip(task_ids, test_lists, outputs)
        ):
            prompt = raw_prompts[idx]
            for comp in output.outputs:
                completion_text = comp.text
                cleaned_code = wrapper(completion_text)
                record = {
                    "task_id": task_id,
                    "generation": cleaned_code,
                    "prompt": prompt,
                    "test_list": test_list,
                }
                samples_for_eval.append(record)
                json.dump(record, f)
                f.write("\n")

    result = evaluate_functional_correctness(
        input_file=samples_path,
        tmp_dir="./temps",
        problem_file=os.path.join("./mbpp_eva", "mbpp_test.jsonl"),
        language="python",
        is_mbpp=True,
        k=[10],
    )

    print(f"📊 {NAME} MBPP Results (Lora={LORA}):")


if __name__ == "__main__":
    NAME = "deepseek-coder-6.7b-instruct"
    LORA = True

    MODEL_PATH = f"LLM_store_path"
    MAX_NEW_TOKENS = 512
    MAX_LENGTH = MAX_NEW_TOKENS + 4468

    print(f"\n🚀 Starting MBPP inference for {NAME}...")
    main(NAME, MODEL_PATH, MAX_LENGTH)
    print(f"✅ Completed {NAME}.\n")
