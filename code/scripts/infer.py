#!/usr/bin/env python
"""Unified vLLM inference (TP=1, single-GPU) for the test set.

Each model is pinned to a single GPU.  Run 3 models in parallel:
    CUDA_VISIBLE_DEVICES=0 python scripts/infer.py --model qwen ... &
    CUDA_VISIBLE_DEVICES=1 python scripts/infer.py --model deepseek ... &
    CUDA_VISIBLE_DEVICES=2 python scripts/infer.py --model codegemma ... &

Outputs:
    {outputs_dir}/{short_name}__{ablation_name}__{adapter_tag}/{decoding}/run{idx}/{folder}/{filename}
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

from cogrpo.prompts import build_prompt_text, build_user_message
from cogrpo.utils import (
    deep_merge,
    ensure_dir,
    extract_code_from_completion,
    load_yaml,
    parse_filename,
)

logger = logging.getLogger(__name__)


def _resolve_folder(test_root: Path, folder: str) -> Path:
    if folder != "blank":
        return test_root / folder
    blank_dir = test_root / "blank"
    return blank_dir if blank_dir.exists() else test_root / "above1"


def collect_test_prompts(test_root: str, folders: List[str], limit: int | None = None):
    items = []
    test_root = Path(test_root)
    for folder in folders:
        folder_dir = _resolve_folder(test_root, folder)
        if not folder_dir.exists():
            logger.warning("Skipping missing folder %s", folder_dir)
            continue
        for fp in sorted(folder_dir.glob("*.py")):
            with open(fp, "r", encoding="utf-8") as f:
                lines = f.readlines()
            try:
                meta = parse_filename(fp.name)
            except ValueError:
                continue
            body = build_prompt_text(lines, completion_line=meta["completion_line"],
                                     missing_lines=meta["co_lines"])
            items.append((folder, fp.name, body))
            if limit is not None and len(items) >= limit:
                return items
    return items


def reconstruct_file(prompt_body: str, code_block: str) -> str:
    """Insert code_block into prompt_body at the `# missing: N lines` placeholder.

    Mirrors vllm10.py's batch_combine: takes the prompt text (which already has
    CO code replaced by `# missing: N lines`), strips the trailing empty line,
    then replaces the placeholder with the generated code.
    """
    lines = prompt_body.splitlines(keepends=True)
    # Remove trailing empty line (from the original prompt construction)
    if lines and not lines[-1].strip():
        lines = lines[:-1]

    # Find and replace the `# missing: N lines` placeholder
    for i, line in enumerate(lines):
        if line.strip().startswith("# missing:"):
            code_lines = code_block.splitlines(keepends=True) or ["pass\n"]
            if not code_lines[-1].endswith("\n"):
                code_lines[-1] += "\n"
            lines[i:i + 1] = code_lines
            break

    body = "".join(lines)
    if not body.lstrip().startswith("# -*- coding:"):
        body = "# -*- coding: utf-8 -*-\n" + body
    return body.replace("\x00", "")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="configs/base.yaml")
    p.add_argument("--model", required=True)
    p.add_argument("--ablation", required=True)
    p.add_argument("--epoch", type=int, default=2)
    p.add_argument("--no_lora", action="store_true")
    p.add_argument("--decoding", default="greedy", choices=["greedy", "low_t", "high_t", "all"])
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--max_model_len", type=int, default=1024)
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s | %(message)s")

    base_cfg = load_yaml(args.base)
    model_cfg = load_yaml(args.model)
    ablation_cfg = load_yaml(args.ablation)
    cfg = deep_merge(base_cfg, {"model": model_cfg, "ablation": ablation_cfg})

    short_name = cfg["model"]["short_name"]
    ablation_name = cfg["ablation"]["name"]
    model_path = cfg["model"]["model_path"]
    folders = cfg["test_folders"]
    test_root = cfg["paths"]["test_dataset_dir"]

    decoding_modes = ["greedy", "low_t", "high_t"] if args.decoding == "all" else [args.decoding]

    # --- LoRA path ---
    adapter_path = None
    adapter_tag = "base"
    if not args.no_lora:
        adapter_path = (
            Path(cfg["paths"]["checkpoints_dir"])
            / f"{short_name}__{ablation_name}" / f"epoch{args.epoch}"
        )
        if not adapter_path.exists():
            logger.warning("Adapter %s not found; falling back to base model", adapter_path)
            adapter_path = None
        else:
            adapter_tag = f"{ablation_name}_e{args.epoch}"

    items = collect_test_prompts(test_root, folders, limit=args.limit)
    if not items:
        logger.error("No test prompts found.")
        return
    logger.info("Will generate for %d items x %d decoding modes (GPU: %s)",
                len(items), len(decoding_modes),
                os.environ.get("CUDA_VISIBLE_DEVICES", "all"))

    # Cache prompt bodies for reconstruction
    prompt_cache: Dict[Tuple[str, str], str] = {}
    for folder, filename, body in items:
        key = (folder, filename)
        if key not in prompt_cache:
            prompt_cache[key] = body

    # --- vLLM (TP=1, single GPU) ---
    from transformers import AutoTokenizer
    from vllm import LLM, SamplingParams
    from vllm.lora.request import LoRARequest

    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    user_messages = [[{"role": "user", "content": build_user_message(body)}] for _, _, body in items]
    formatted_prompts = tokenizer.apply_chat_template(user_messages, tokenize=False, add_generation_prompt=True)

    use_lora = adapter_path is not None
    # Always eager for power stability on this server.

    llm = LLM(
        model=model_path,
        trust_remote_code=True,
        tensor_parallel_size=1,
        max_model_len=args.max_model_len,
        dtype="auto",
        enable_lora=use_lora,
        enforce_eager=True,
        gpu_memory_utilization=0.85,
        max_num_seqs=64,
    )
    lora_req = LoRARequest("cogrpo", 1, str(adapter_path)) if use_lora else None

    out_root = Path(cfg["paths"]["outputs_dir"]) / f"{short_name}__{ablation_name}__{adapter_tag}"

    for mode in decoding_modes:
        dcfg = cfg["decoding"][mode]
        for run_idx in range(dcfg["repeats"]):
            sp_kwargs = dict(
                temperature=dcfg.get("temperature", 0.0),
                max_tokens=dcfg.get("max_tokens", 256),
                seed=42 + run_idx,
            )
            if "top_p" in dcfg and dcfg["top_p"] is not None:
                sp_kwargs["top_p"] = dcfg["top_p"]
            sp = SamplingParams(**sp_kwargs)
            outputs = llm.generate(formatted_prompts, sp, lora_request=lora_req) if lora_req else llm.generate(formatted_prompts, sp)

            for (folder, filename, _body), out in zip(items, outputs):
                text = out.outputs[0].text
                code_block = extract_code_from_completion(text)
                content = reconstruct_file(prompt_cache[(folder, filename)], code_block)
                out_dir = out_root / mode / f"run{run_idx}" / folder
                ensure_dir(out_dir)
                (out_dir / filename).write_text(content, encoding="utf-8")
            logger.info("Decoding=%s run=%d done", mode, run_idx)


if __name__ == "__main__":
    main()
