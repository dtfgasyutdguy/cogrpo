#!/usr/bin/env python
"""Probe the largest viable batch size for a given (model, ablation).

Strategy:
    For each candidate batch_size in --candidates, run a 2-step training
    smoke on a single GPU, monitor peak memory, record success/OOM. Print
    a table at the end with the max safe batch size and peak memory.

Single-GPU on purpose â€?we measure per-device. Multiply by num_processes
for the effective batch when launching with accelerate.

Usage:
    /path/to/cogrpo/w/bin/python scripts/tune_batch_size.py \
        --model configs/models/qwen.yaml \
        --ablation configs/ablation/full.yaml \
        --candidates 4 6 8 10 12 14
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def make_tmp_yaml(model_yaml: str, batch_size: int) -> str:
    with open(model_yaml, "r") as f:
        m = yaml.safe_load(f)
    m["batch_size_per_device"] = batch_size
    fd, tmp = tempfile.mkstemp(suffix=".yaml")
    os.close(fd)
    with open(tmp, "w") as f:
        yaml.safe_dump(m, f)
    return tmp


def run_one(
    base: str,
    model_yaml: str,
    ablation_yaml: str,
    batch_size: int,
    gpu_id: int = 0,
    max_steps: int = 2,
):
    tmp = make_tmp_yaml(model_yaml, batch_size)
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
    env["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    cmd = [
        "/path/to/cogrpo/w/bin/python", str(Path(__file__).parent / "train.py"),
        "--base", base,
        "--model", tmp,
        "--ablation", ablation_yaml,
        "--epoch", "1",
        "--max_steps", str(max_steps),
    ]
    t0 = time.time()
    proc = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=900)
    dur = time.time() - t0

    out = proc.stdout + "\n" + proc.stderr
    success = proc.returncode == 0
    oom = "CUDA out of memory" in out or "OutOfMemoryError" in out

    # Try to extract loss / coir_loss / peak memory
    # Peak memory is best read via nvidia-smi during the run; here we look
    # for the OOM message itself (which often reports current usage).
    last_lines = "\n".join(out.splitlines()[-20:])

    return {
        "batch_size": batch_size,
        "success": success and not oom,
        "oom": oom,
        "duration_s": round(dur, 1),
        "tail": last_lines[:1500],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="configs/base.yaml")
    p.add_argument("--model", required=True)
    p.add_argument("--ablation", default="configs/ablation/full.yaml")
    p.add_argument("--candidates", nargs="+", type=int,
                   default=[4, 6, 8, 10, 12, 14])
    p.add_argument("--gpu", type=int, default=0)
    p.add_argument("--max_steps", type=int, default=2)
    p.add_argument("--output", default=None)
    args = p.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(message)s",
    )

    candidates = sorted(set(args.candidates))
    results = []
    print(f"\n{'=' * 70}")
    print(f"Probing batch sizes for {args.model} | {args.ablation}")
    print(f"Candidates: {candidates}")
    print(f"{'=' * 70}\n")

    for bs in candidates:
        print(f">>> trying batch_size = {bs}")
        r = run_one(args.base, args.model, args.ablation, bs, args.gpu, args.max_steps)
        ok = "OK" if r["success"] else ("OOM" if r["oom"] else "FAIL")
        print(f"    [{ok}] duration={r['duration_s']}s")
        results.append(r)
        # Stop the moment we hit OOM
        if r["oom"]:
            break

    # Summary
    print(f"\n{'=' * 70}\nSUMMARY\n{'=' * 70}")
    print(f"{'batch_size':>12} | {'status':>8} | {'duration_s':>10}")
    for r in results:
        status = "OK" if r["success"] else ("OOM" if r["oom"] else "FAIL")
        print(f"{r['batch_size']:>12} | {status:>8} | {r['duration_s']:>10}")

    safe = [r for r in results if r["success"]]
    if safe:
        recommended = max(r["batch_size"] for r in safe)
        print(f"\n>>> Recommended batch_size_per_device: {recommended}")
    else:
        print("\n>>> No batch size worked; reduce gradient_accumulation or model size.")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
