## Project Structure
data and code for CO-GRPO

```
cogrpo/
├── README.md
├── generate/
│   ├── COGRPO_generate.tar.gz          (greedy decoding results)
│   └── high_low_temp.tar.gz                (high/low temperature sampling results)
├── lora_parameter/
│   ├── codegemma-1.1-7b-it/epoch1/     (adapter_config.json + adapter_model.safetensors)
│   ├── deepseek-coder-6.7b-instruct/epoch1/
│   └── Qwen2.5-Coder-7B-Instruct/epoch1/
├── dataset/
│   ├── Eval/                           (1,000-sample evaluation set, 17 position variants + blank)
│   └── Train/                          (400-sample training set x3 segments = 1,200 files)
└── code/
    ├── cogrpo/                         (core CO-GRPO module)
    │   ├── CO_CR.py                    (reward function with CodeQL + CO-CR)
    │   ├── codeql_runner.py            (CodeQL database creation and analysis)
    │   ├── util.py                     (infer construction)
    │   └── utils.py                    (utility functions)
    ├── configs/
    │   ├── base.yaml                   (global configuration)
    │   └── models/                     (per-model configurations)
    │       ├── qwen.yaml
    │       ├── deepseek.yaml
    │       └── codegemma.yaml
    ├── scripts/
    │   ├── train.py                    (CO-GRPO training entry point)
    │   ├── prepare_data.py             (build paired training JSONL)
    │   ├── compute_cocr_reference.py   (pre-compute CO-CR reference data)
    │   ├── infer.py                    (batch inference over test prompts)
    │   ├── score.py                    (CodeQL-based defect scoring)
    │   ├── eval_humaneval.py           (HumanEval pass@1/pass@10 evaluation)
    │   ├── eval_mbpp.py                (MBPP pass@1/pass@10 evaluation)
    │   └── tune_batch_size.py          (batch size probing)
    ├── human-eval.py                   (consolidated HumanEval evaluation)
    ├── mbpp.py                         (consolidated MBPP evaluation)
    ├── human-eval/                     (HumanEval evaluation framework)
    ├── mbpp_eva/                       (MBPP evaluation framework)
    ├── pass@10/                        (pass@10 computation scripts)
    ├── codeql_analyze.py               (standalone CodeQL analysis)
    ├── all-security-selectors.yml      (CodeQL security selectors)
    ├── python-security-all.qls         (CodeQL query suite)
    └── requirements.txt
```

## Overview

CO-GRPO fine-tunes LLMs to resist defective CO (Copilot-originated) code influence. Given a code completion prompt contaminated with defective CO code, the model learns to produce clean completions. The method combines GRPO with a CodeQL-based reward function and a **CO-CR (CO-Code Contrastive Reward)** mechanism that penalizes completions where the CO code context induces a CWE that would not appear in a clean context.

## Quick Start

### Environment
- Python 3.11, Ubuntu 22.04, 4x NVIDIA RTX 3090
- Install dependencies: `pip install -r requirements.txt`

### CodeQL Setup
```bash
# Download CodeQL CLI
# https://github.com/github/codeql-cli-binaries/releases
git clone https://github.com/github/codeql.git
# Copy rule configs to the CodeQL directory
cp code/all-security-selectors.yml codeql/ql/misc/suite-helpers/
cp code/python-security-all.qls codeql/ql/python/ql/src/codeql-suites/
```

### Training
```bash
# Step 1: Build paired training data
python scripts/prepare_data.py

# Step 2: Pre-compute CO-CR reference
python scripts/compute_cocr_reference.py

# Step 3: Train (single GPU)
python scripts/train.py --model configs/models/qwen.yaml --epoch 1

# Step 3: Train (4-GPU DDP)
accelerate launch --multi_gpu --num_processes=4 \
    scripts/train.py --model configs/models/qwen.yaml --epoch 1
```

### Evaluation
```bash
# Defect analysis on generated code
python scripts/score.py

# Code capability evaluation
python scripts/eval_humaneval.py
python scripts/eval_mbpp.py
```

## Models

| Model | HuggingFace ID |
|-------|---------------|
| Qwen | Qwen2.5-Coder-7B-Instruct |
| DeepSeek | deepseek-coder-6.7b-instruct |
| CodeGemma | codegemma-1.1-7b-it |