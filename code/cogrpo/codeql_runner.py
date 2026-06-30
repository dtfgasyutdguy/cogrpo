from __future__ import annotations

import csv
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

import pandas as pd


logger = logging.getLogger(__name__)


def compile_query_suite(codeql_bin: str, suite: str) -> None:
    """One-time compile of the CodeQL query suite (idempotent)."""
    subprocess.run(
        [codeql_bin, "query", "compile", "--threads=39", "--quiet", suite],
        check=True,
        stdout=subprocess.DEVNULL,
    )


def _reset_dir(path: str | Path) -> None:
    p = Path(path)
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)


def run_codeql_analysis(
    src_folder: str | Path,
    db_path: str | Path,
    codeql_bin: str,
    suite: str,
    timeout_sec: int = 5,
    threads: int = 10,
) -> Path | None:
    """Run CodeQL on `src_folder`, returning the path to the result CSV.

    Returns None if there are no .py files to scan.
    """
    src_folder = Path(src_folder)
    if not src_folder.exists() or not any(src_folder.iterdir()):
        return None

    output_csv = src_folder / "codeql_analysis_results.csv"
    if output_csv.exists():
        output_csv.unlink()

    _reset_dir(db_path)

    try:
        subprocess.run(
            [
                codeql_bin, "database", "create", str(db_path),
                "--language=python", "--overwrite", "--quiet",
                "--source-root", str(src_folder),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                codeql_bin, "database", "analyze", str(db_path), suite,
                f"--timeout={timeout_sec}", f"--threads={threads}",
                "--format=csv", "--quiet",
                "--output", str(output_csv),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        logger.warning("CodeQL failed for %s: %s", src_folder, e)
        return None
    finally:
        if Path(db_path).exists():
            shutil.rmtree(db_path)

    return output_csv if output_csv.exists() else None


def parse_codeql_csv(csv_path) -> pd.DataFrame:
    """Parse the raw CodeQL CSV into a DataFrame with extracted file metadata.

    Output columns:
        cwe_str            CodeQL rule name
        filename           "{sample_id}_{a}_{completion_line}_{c}.py"
        sample_id          int
        seq                int (training-time: G index; test-time: a)
        completion_line    int (filename field 3, may be -1 if absent)
        detect_start_line  int (line CodeQL flagged)
        start_line         alias of detect_start_line (legacy)
    """
    csv_path = Path(csv_path)
    if not csv_path.exists() or csv_path.stat().st_size == 0:
        return pd.DataFrame()

    raw = pd.read_csv(csv_path, header=None)
    if raw.empty:
        return pd.DataFrame()

    raw = raw.iloc[:, [0, 4, 5]].drop_duplicates(keep="first")
    raw.columns = ["cwe_str", "filename", "detect_start_line"]
    raw["filename"] = raw["filename"].str.lstrip("/")
    parts = raw["filename"].str.replace(".py", "", regex=False).str.split("_", expand=True)
    if parts.shape[1] < 2:
        return pd.DataFrame()

    raw["sample_id"] = pd.to_numeric(parts[0], errors="coerce").astype("Int64")
    raw["seq"] = pd.to_numeric(parts[1], errors="coerce").astype("Int64")
    if parts.shape[1] >= 3:
        raw["completion_line"] = pd.to_numeric(parts[2], errors="coerce").astype("Int64")
    else:
        raw["completion_line"] = pd.NA
    raw = raw.dropna(subset=["sample_id", "seq"])
    raw["sample_id"] = raw["sample_id"].astype(int)
    raw["seq"] = raw["seq"].astype(int)
    raw["completion_line"] = raw["completion_line"].fillna(-1).astype(int)
    raw["detect_start_line"] = raw["detect_start_line"].astype(int)
    raw["start_line"] = raw["detect_start_line"]   # legacy alias
    return raw


def run_codeql_evaluation(
    src_folder: str | Path,
    db_path: str | Path,
    codeql_bin: str,
    suite: str,
    timeout_sec: int = 10,
    threads: int = 39,
) -> int:
    """Used by scripts/score.py: scan a generation folder and return total raw findings."""
    csv_path = run_codeql_analysis(
        src_folder, db_path, codeql_bin, suite, timeout_sec, threads,
    )
    if csv_path is None:
        return 0
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        return sum(1 for _ in csv.reader(f))
