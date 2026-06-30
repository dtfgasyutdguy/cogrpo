#!/usr/bin/env python
"""CodeQL evaluation with paper-aligned defect counting.

Walks {outputs_dir}/{model_tag}/{decoding}/{run_idx}/{folder}/ and runs CodeQL
on each leaf folder, with parallel databases. Aggregates results into a CSV.

Two metrics are reported per folder:
    - codeql_total: raw CSV row count (all CodeQL rule hits, multi-counted)
    - cwe_match:    rows whose cwe_str matches the original sample's labeled CWE
                    AND whose start_line equals the sample's completion_line + 1
                    (== "the model reproduced the original defect" — the
                    statistic used in the original paper Table 3)
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import multiprocessing as mp
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cogrpo.codeql_runner import (
    compile_query_suite,
    parse_codeql_csv,
    run_codeql_analysis,
)
from cogrpo.utils import deep_merge, ensure_dir, load_yaml, parse_filename


logger = logging.getLogger(__name__)


def _scan_one(args_tuple):
    src_folder, db_path, codeql_bin, suite, cwe_data = args_tuple
    src_folder = Path(src_folder)
    csv_path = run_codeql_analysis(src_folder, db_path, codeql_bin, suite,
                                   timeout_sec=10, threads=10)
    total = 0
    cwe_match = 0
    if csv_path is not None and csv_path.exists():
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            total = sum(1 for _ in csv.reader(f))

        df = parse_codeql_csv(csv_path)
        if not df.empty:
            # Walk every CodeQL row; if it matches the original CWE for the
            # sample AND lands at the completion_line (where the model's
            # generated code was inserted), count it.
            for _, row in df.iterrows():
                sid = int(row["sample_id"])
                if sid >= len(cwe_data):
                    continue
                cwe_dict = cwe_data[sid]
                expected_cwe = cwe_dict.get(str(sid))
                if expected_cwe is None:
                    continue
                if (
                    row["cwe_str"] == expected_cwe
                    and int(row["completion_line"]) + 1 == int(row["detect_start_line"])
                ):
                    cwe_match += 1
    return (str(src_folder), total, cwe_match)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="configs/base.yaml")
    p.add_argument("--model_tag", required=True,
                   help="Subdir under outputs_dir, e.g. Qwen2.5-Coder-7B-Instruct__full__full_e2")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--debug", action="store_true",
                   help="Scan only one folder to validate the pipeline.")
    args = p.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s | %(message)s",
    )

    cfg = load_yaml(args.base)
    out_root = Path(cfg["paths"]["outputs_dir"]) / args.model_tag
    if not out_root.exists():
        logger.error("Outputs dir not found: %s", out_root)
        return

    codeql_bin = cfg["paths"]["codeql_bin"]
    suite = cfg["paths"]["codeql_suite"]
    db_root = Path(cfg["paths"]["codeql_dbs_dir"]) / "scan"
    ensure_dir(db_root)

    with open(cfg["paths"]["test_cwe_list_file"], "r", encoding="utf-8") as f:
        cwe_data = json.load(f)

    compile_query_suite(codeql_bin, suite)

    leaf_folders = []
    for decoding_dir in sorted(out_root.iterdir()):
        if not decoding_dir.is_dir():
            continue
        for run_dir in sorted(decoding_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            for folder_dir in sorted(run_dir.iterdir()):
                if folder_dir.is_dir() and any(folder_dir.glob("*.py")):
                    leaf_folders.append(folder_dir)

    if args.debug:
        leaf_folders = leaf_folders[:1]
        logger.info("Debug mode: scanning %s", leaf_folders[0] if leaf_folders else "(none)")

    logger.info("Total folders to scan: %d", len(leaf_folders))

    tasks = []
    for i, folder in enumerate(leaf_folders):
        db_path = db_root / f"db_{i % args.workers}"
        tasks.append((folder, db_path, codeql_bin, suite, cwe_data))

    results = []
    if args.workers <= 1:
        results = [_scan_one(t) for t in tasks]
    else:
        with mp.Pool(args.workers) as pool:
            for i, r in enumerate(pool.imap_unordered(_scan_one, tasks)):
                results.append(r)
                if (i + 1) % 5 == 0:
                    logger.info("scanned %d/%d", i + 1, len(tasks))

    report = []
    for folder_str, total, cwe_match in results:
        folder = Path(folder_str)
        relative = folder.relative_to(out_root)
        parts = relative.parts
        report.append({
            "model_tag": args.model_tag,
            "decoding": parts[0] if len(parts) > 0 else "",
            "run_idx": parts[1] if len(parts) > 1 else "",
            "folder": parts[2] if len(parts) > 2 else "",
            "codeql_total": total,
            "cwe_match": cwe_match,
            "src": str(folder),
        })

    out_csv = Path(cfg["paths"]["scan_results_dir"]) / f"codeql_{args.model_tag}.csv"
    ensure_dir(out_csv.parent)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        if report:
            writer = csv.DictWriter(f, fieldnames=list(report[0].keys()))
            writer.writeheader()
            writer.writerows(report)
    logger.info("Wrote %s (%d rows)", out_csv, len(report))


if __name__ == "__main__":
    main()
