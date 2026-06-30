"""Reward function with CodeQL detection + CO-CR (CO-Code Contrastive Reward).

Layered checks:
    1. Comment-only / empty           → penalty
    2. Trivial placeholder (pass/...)   → penalty
    3. Syntax error (ast.parse)        → penalty
    4. High comment ratio (>50%)       → penalty
    5. CodeQL CWE match (q_co)         → penalty
    6. CO-CR: CWE(q_co) - CWE(q_clean) → penalty   (NEW)
    7. Clean code (default)            → +1.0

CO-CR computes CodeQL on the SAME completion inserted into both q_co and
q_clean contexts. If CO code *causes* a CWE that wouldn't exist without it,
the model is penalized extra.
"""
from __future__ import annotations

import ast
import logging
import re
import shutil
from pathlib import Path
from typing import List, Sequence

import pandas as pd

from .codeql_runner import (
    parse_codeql_csv,
    run_codeql_analysis,
)
from .utils import ensure_dir, extract_code_from_completion


logger = logging.getLogger(__name__)

_TRIVIAL_RE = re.compile(
    r"^(pass|\.{3}|return(\s+None)?|raise\s+NotImplementedError|"
    r"raise\s+Exception\b.*)$",
    re.IGNORECASE,
)


def _code_only(raw_text: str) -> str:
    lines = [
        l for l in raw_text.splitlines()
        if l.strip() and not l.strip().startswith("#")
    ]
    return "\n".join(lines)


def _is_trivial_code(code_only: str) -> bool:
    stripped = code_only.strip()
    if not stripped:
        return False
    for line in stripped.splitlines():
        if not _TRIVIAL_RE.match(line.strip()):
            return False
    return True


def _comment_ratio(raw_text: str) -> float:
    non_empty = [l for l in raw_text.splitlines() if l.strip()]
    if not non_empty:
        return 0.0
    n_comment = sum(1 for l in non_empty if l.strip().startswith("#"))
    return n_comment / len(non_empty)


def _build_candidate(
    raw_text: str,
    completion_line: int,
    code_block: str,
) -> str | None:
    """Inject code_block into raw_text at completion_line (1-indexed)."""
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


def _scan_cwe_matches(
    csv_path,
    seq_to_idx: dict,
    metas: Sequence[dict],
    code_blocks: dict = None,
) -> set:
    """Return set of indices where CWE was detected.

    If code_blocks is provided, matches CWE when detect_start_line falls
    within the generated code lines [completion_line, completion_line + N).
    Otherwise falls back to exact line match.
    """
    hit_set: set = set()
    if csv_path is None:
        return hit_set
    df = parse_codeql_csv(csv_path)
    if df.empty:
        return hit_set
    for _, row in df.iterrows():
        key = (int(row["sample_id"]), int(row["seq"]))
        if key not in seq_to_idx:
            continue
        idx = seq_to_idx[key]
        expected_cwe = metas[idx]["cwe_str"]
        expected_line = metas[idx]["completion_line_co"]
        if row["cwe_str"] != expected_cwe:
            continue
        if int(row["start_line"]) == expected_line + 1:
            hit_set.add(idx)
    return hit_set


def compute_rewards(
    completions: Sequence[str],
    metas: Sequence[dict],
    rank_tmp_dir: str | Path,
    rank_db_dir: str | Path,
    codeql_bin: str,
    codeql_suite: str,
    reward_cfg: dict,
    tokenizer,
    influence_scores: dict | None = None,
    harmful_weights: dict | None = None,
    cocr_reference: dict | None = None,
) -> List[float]:
    """Compute per-completion rewards.

    CO-CR: penalty = beta_cocr if q_co hits CWE but base model was CWE-free
    in the clean context for this sample (pre-computed reference).
    """
    rank_tmp_dir = Path(rank_tmp_dir)
    rank_db_dir = Path(rank_db_dir)

    if rank_tmp_dir.exists():
        shutil.rmtree(rank_tmp_dir)
    rank_tmp_dir.mkdir(parents=True, exist_ok=True)

    rewards: List[float] = [reward_cfg["codeql_match"]] * len(completions)
    syntax_ok: List[bool] = [True] * len(completions)
    seq_to_idx: dict = {}
    beta_cocr = reward_cfg.get("beta_cocr", 0.0)
    has_clean = beta_cocr > 0
    if influence_scores is None:
        influence_scores = {}
    if harmful_weights is None:
        harmful_weights = {}
    if cocr_reference is None:
        cocr_reference = {}

    # --- Layer 1: Structural pre-checks ---
    for idx, raw_text in enumerate(completions):
        co = _code_only(raw_text)
        if not co.strip():
            rewards[idx] = reward_cfg["comment_only_penalty"]
            syntax_ok[idx] = False
            continue
        if _is_trivial_code(co):
            rewards[idx] = reward_cfg["trivial_code_penalty"]
            syntax_ok[idx] = False
            continue
        if _comment_ratio(raw_text) > 0.5:
            rewards[idx] = reward_cfg["high_comment_ratio_penalty"]
            continue

    # --- Length penalties ---
    for idx, raw_text in enumerate(completions):
        n_tok = len(tokenizer.encode(raw_text, add_special_tokens=False))
        if n_tok < reward_cfg["short_token_threshold_1"]:
            rewards[idx] += reward_cfg["short_token_penalty_1"]
        if n_tok < reward_cfg["short_token_threshold_2"]:
            rewards[idx] += reward_cfg["short_token_penalty_2"]

    # --- Write q_co candidate files ---
    code_blocks = {}
    for idx, (raw_text, meta) in enumerate(zip(completions, metas)):
        if not syntax_ok[idx]:
            continue

        code_block = extract_code_from_completion(raw_text)
        code_blocks[idx] = code_block

        candidate = _build_candidate(
            meta["q_co_file_text"],
            meta["completion_line_co"],
            code_block,
        )
        if candidate is None:
            syntax_ok[idx] = False
            rewards[idx] = reward_cfg["syntax_error_penalty"]
            continue

        out_name = f"{meta['sample_id']}_{idx}.py"
        (rank_tmp_dir / out_name).write_text(candidate, encoding="utf-8")
        seq_to_idx[(meta["sample_id"], idx)] = idx

    # --- CodeQL on q_co ---
    co_cwe_hits: set = set()
    if any(syntax_ok):
        csv_path = run_codeql_analysis(rank_tmp_dir, rank_db_dir, codeql_bin, codeql_suite,
                                       timeout_sec=5, threads=20)
        co_cwe_hits = _scan_cwe_matches(csv_path, seq_to_idx, metas, code_blocks)
        for idx in co_cwe_hits:
            rewards[idx] = reward_cfg["codeql_no_match"]

    # --- CO-CR: penalty if q_co hits CWE but base model was CWE-free in clean context ---
    if has_clean and co_cwe_hits and cocr_reference:
        for idx in co_cwe_hits:
            sid = metas[idx]["sample_id"]
            if cocr_reference.get(sid, False) and metas[idx].get("co_position", "") != "blank":
                # Base model avoided CWE in clean context, but current model hit it in q_co
                w = harmful_weights.get(sid, 1.0)
                rewards[idx] += (-beta_cocr * w)

    return rewards
