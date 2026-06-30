#!/usr/bin/env python
"""Compute CO-CR reference: base model CWE status on q_clean context."""
from __future__ import annotations

import argparse, json, logging, shutil, sys
from pathlib import Path

sys.path.insert(0, "/path/to/cogrpo")

from cogrpo.codeql_runner import run_codeql_analysis, parse_codeql_csv, compile_query_suite
from cogrpo.utils import load_yaml, deep_merge, ensure_dir, jsonl_iter, extract_code_from_completion

logger = logging.getLogger(__name__)


def _build_candidate(raw_text: str, completion_line: int, code_block: str) -> str | None:
    import ast
    lines = raw_text.splitlines(keepends=True)
    if completion_line < 1 or completion_line > len(lines) + 1:
        return None
    code_lines = code_block.splitlines(keepends=True) or ["pass\n"]
    if not code_lines[-1].endswith("\n"):
        code_lines[-1] = code_lines[-1] + "\n"
    assembled = (
        "# -*- coding: utf-8 -*-\n"
        + "".join(lines[: completion_line - 1])
        + "".join(code_lines)
        + "".join(lines[completion_line:])
    )
    if "\x00" in assembled:
        assembled = assembled.replace("\x00", "")
    try:
        ast.parse(assembled)
    except SyntaxError:
        return None
    return assembled


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="configs/base.yaml")
    p.add_argument("--model", required=True)
    p.add_argument("--ablation", required=True)
    p.add_argument("--output", default=None, help="Output JSON path")
    p.add_argument("--n_generations", type=int, default=4)
    p.add_argument("--max_new_tokens", type=int, default=160)
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()

    base_cfg = load_yaml(args.base)
    model_cfg = load_yaml(args.model)
    ablation_cfg = load_yaml(args.ablation)
    cfg = deep_merge(base_cfg, {"model": model_cfg, "ablation": ablation_cfg})

    short_name = cfg["model"]["short_name"]
    pairs_file = cfg["paths"]["pairs_file"]
    codeql_bin = cfg["paths"]["codeql_bin"]
    codeql_suite = cfg["paths"]["codeql_suite"]
    model_path = cfg["model"]["model_path"]

    records = list(jsonl_iter(pairs_file))
    if args.limit:
        records = records[:args.limit]
    n = len(records)
    logger.info("Computing CO-CR reference for %d samples (G=%d)", n, args.n_generations)

    with open(cfg["paths"]["cwe_list_file"]) as f:
        cwe_data = json.load(f)
    cwe_map = {}
    for i, entry in enumerate(cwe_data):
        cwe_map[i] = entry.get(str(i), "")

    cl_texts = {}
    cl_lines = {}
    for r in records:
        sid = r["sample_id"]
        if sid not in cl_texts:
            with open(r["q_clean_file"], "r") as f:
                cl_texts[sid] = f.read()
            cl_lines[sid] = r.get("completion_line_clean", r["completion_line_co"])

    from vllm import LLM, SamplingParams
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side="left")
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    cl_messages = [[{"role": "user", "content": r["q_clean_user"]}] for r in records]
    cl_prompts = tokenizer.apply_chat_template(
        cl_messages, tokenize=False, add_generation_prompt=True,
    )

    logger.info("Loading base model vLLM (no LoRA)...")
    llm = LLM(
        model=model_path, trust_remote_code=True, tensor_parallel_size=1,
        max_model_len=1024, dtype="auto", enable_lora=False,
        gpu_memory_utilization=0.85, max_num_seqs=32, enforce_eager=True,
    )
    sp = SamplingParams(temperature=0.7, top_p=0.8, top_k=20,
                        n=args.n_generations, max_tokens=args.max_new_tokens, seed=42)

    logger.info("Generating %d x %d completions on q_clean...", n, args.n_generations)
    outputs = llm.generate(cl_prompts, sp)

    completions = {}
    for rec, out in zip(records, outputs):
        sid = rec["sample_id"]
        if sid not in completions:
            completions[sid] = []
        for sub in out.outputs[:args.n_generations]:
            code = extract_code_from_completion(sub.text)
            completions[sid].append(code)

    del llm, outputs
    import gc, torch
    gc.collect()
    torch.cuda.empty_cache()

    compile_query_suite(codeql_bin, codeql_suite)
    tmp_base = Path(cfg["paths"]["tmp_dir"]) / "cocr_reference"
    cl_dir = tmp_base / "cl"
    if cl_dir.exists():
        shutil.rmtree(cl_dir)
    cl_dir.mkdir(parents=True, exist_ok=True)

    sample_ids = set(r["sample_id"] for r in records)
    for sid in sorted(sample_ids):
        cl_cl = cl_lines.get(sid, 1)
        for seq, code in enumerate(completions.get(sid, [])):
            cl_cand = _build_candidate(cl_texts.get(sid, ""), cl_cl, code)
            if cl_cand:
                (cl_dir / f"{sid}_{seq}_{cl_cl}.py").write_text(cl_cand, encoding="utf-8")

    logger.info("Running CodeQL on %d clean files...", len(list(cl_dir.glob("*.py"))))
    cl_csv = run_codeql_analysis(cl_dir, tmp_base / "db_cl", codeql_bin, codeql_suite,
                                  timeout_sec=10, threads=20)

    df = parse_codeql_csv(cl_csv) if cl_csv else None
    cwe_hit_sids = set()

    if df is not None and not df.empty:
        parts = df["filename"].str.replace(".py", "", regex=False).str.split("_", expand=True)
        df["sample_id"] = parts[0].astype(int)
        df["completion_line"] = parts[2].astype(int)
        for _, row in df.iterrows():
            sid = int(row["sample_id"])
            if sid not in sample_ids:
                continue
            expected_cwe = cwe_map.get(sid, "")
            if not expected_cwe or row["cwe_str"] != expected_cwe:
                continue
            if int(row["start_line"]) == int(row["completion_line"]) + 1:
                cwe_hit_sids.add(sid)

    reference = {}
    for r in records:
        sid = r["sample_id"]
        reference[sid] = sid not in cwe_hit_sids

    n_clean_free = sum(1 for v in reference.values() if v)
    logger.info("CO-CR reference: %d/%d samples are CWE-free in clean context", n_clean_free, n)

    output_path = args.output
    if output_path is None:
        output_path = Path(cfg["paths"]["data_dir"]) / "cocr_reference" / f"{short_name}.json"
    ensure_dir(Path(output_path).parent)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(reference, f, ensure_ascii=False, indent=2)
    logger.info("Saved CO-CR reference to %s", output_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")
    main()
