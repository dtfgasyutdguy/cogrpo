#!/usr/bin/env python
"""Build the paired (q_clean, q_co) training JSONL.

Run once before any training. Output: <data>/pairs/train.jsonl
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Make the cogrpo package importable when running from /path/to/cogrpo
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cogrpo.data import build_pairs
from cogrpo.utils import load_yaml


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/base.yaml")
    p.add_argument("--limit", type=int, default=None,
                   help="Cap base sample count (for smoke tests).")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s | %(message)s")

    cfg = load_yaml(args.config)
    paths = cfg["paths"]
    n = build_pairs(
        raw_dir=paths["raw_dataset_dir"],
        cwe_list_file=paths["cwe_list_file"],
        kind_list_file=paths["kind_list_file"],
        output_jsonl=paths["pairs_file"],
        limit=args.limit,
    )
    print(f"Wrote {n} paired records.")


if __name__ == "__main__":
    main()
