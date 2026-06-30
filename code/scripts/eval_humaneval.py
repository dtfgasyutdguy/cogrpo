#!/usr/bin/env python
"""HumanEval evaluation for all 6 models: pass@1 (greedy) + pass@10 (temp=0.8, n=10)."""
import json, sys, os, gzip
sys.path.insert(0, '/path/to/cogrpo')
from pathlib import Path
from vllm import LLM, SamplingParams
from vllm.lora.request import LoRARequest
from transformers import AutoTokenizer

HUMANEVAL_DIR = '/path/to/inference/human-eval'
OUT_DIR = Path('/path/to/cogrpo/humaneval_results')
TMPDIR = '/path/to/cogrpo/tmp'
os.environ['TMPDIR'] = TMPDIR

with gzip.open(f'{HUMANEVAL_DIR}/data/HumanEval.jsonl.gz', 'rb') as f:
    problems = [json.loads(l) for l in f]
print(f'Loaded {len(problems)} HumanEval problems')

CONFIGS = [
    ('greedy', SamplingParams(temperature=0.0, n=1, max_tokens=256, seed=42)),
    ('pass10', SamplingParams(temperature=0.8, top_p=0.95, n=10, max_tokens=256, seed=42)),
]

MODELS = [
    ('Qwen2.5-Coder-7B-Instruct', '/path/to/cogrpo/models/Qwen2.5-Coder-7B-Instruct', 'Qwen2.5-Coder-7B-Instruct'),
    ('deepseek-coder-6.7b-instruct', '/path/to/cogrpo/models/deepseek-coder-6.7b-instruct', 'deepseek-coder-6.7b-instruct'),
    ('codegemma-1.1-7b-it', '/path/to/cogrpo/models/codegemma-1.1-7b-it', 'codegemma-1.1-7b-it'),
]

for model_name, model_path, short_name in MODELS:
    tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side='left')
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    prompts = [p['prompt'] for p in problems]
    formatted = tokenizer.apply_chat_template(
        [[{'role': 'user', 'content': p}] for p in prompts],
        tokenize=False, add_generation_prompt=True
    )

    for ablation, adapter_suffix in [('base', f'{short_name}__base/epoch1'), ('finetuned', f'{short_name}__finetuned/epoch1')]:
        adapter_path = f'/path/to/cogrpo/cogrpo/checkpoints/{adapter_suffix}'
        if not Path(adapter_path).exists():
            print(f'SKIP {short_name}/{ablation}')
            continue

        for cfg_name, sp in CONFIGS:
            print(f'{short_name}/{ablation}/{cfg_name}...')
            llm = LLM(model=model_path, trust_remote_code=True, tensor_parallel_size=1,
                      max_model_len=1024, dtype='auto', enable_lora=True,
                      gpu_memory_utilization=0.85, max_num_seqs=32, enforce_eager=True)
            lora_req = LoRARequest('eval', 1, adapter_path)
            outputs = llm.generate(formatted, sp, lora_request=lora_req)

            samples = []
            for prob, out in zip(problems, outputs):
                for i, sub in enumerate(out.outputs):
                    samples.append({
                        'task_id': prob['task_id'],
                        'completion': sub.text,
                        'sample_id': i,
                    })

            out_file = OUT_DIR / f'{short_name}_{ablation}_{cfg_name}.jsonl'
            with open(out_file, 'w') as f:
                for s in samples:
                    f.write(json.dumps(s) + '\n')
            print(f'  �?{out_file} ({len(samples)} samples)')

            del llm
            import gc, torch
            gc.collect()
            torch.cuda.empty_cache()
