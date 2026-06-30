from __future__ import annotations

import re
import string
import json
import os
from pathlib import Path
from typing import Any

import yaml


_WHITESPACE_TRANSLATOR = str.maketrans("", "", string.whitespace)


def strip_whitespace(text: str) -> str:
    """Remove all whitespace characters (used for keyword sniffing in reward)."""
    return text.translate(_WHITESPACE_TRANSLATOR)


def strip_blank_lines(message: str) -> str:
    """Trim leading blank/comment-only lines from a code completion."""
    if not message:
        return "pass\n"
    lines = message.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return "\n".join(lines[i:])
    return "pass\n"


_PYTHON_BLOCK_RE = re.compile(r"```python(.*?)```", re.DOTALL)
_GENERIC_BLOCK_RE = re.compile(r"```(.*?)```", re.DOTALL)
_PYTHON_TAG_RE = re.compile(r"\[PYTHON\](.*?)\[/PYTHON", re.DOTALL)


def extract_code_from_completion(message: str) -> str:
    """Pull a Python code block out of a model completion.

    Handles ``` python fences, plain ``` fences, [PYTHON] tags, and
    completions where the closing fence is missing.
    """
    if not message:
        return "pass\n"

    m = _PYTHON_BLOCK_RE.search(message)
    if m:
        return strip_blank_lines(m.group(1))

    m = _GENERIC_BLOCK_RE.search(message)
    if m:
        return strip_blank_lines(m.group(1))

    for prefix in ("```python", "```"):
        if message.startswith(prefix):
            return strip_blank_lines(message[len(prefix):])
        idx = message.find(prefix)
        if idx != -1:
            return strip_blank_lines(message[idx + len(prefix):])

    m = _PYTHON_TAG_RE.search(message)
    if m:
        return strip_blank_lines(m.group(1))

    return strip_blank_lines(message)


def count_visual_indent(line: str, tab_size: int = 4) -> int:
    """Count leading visual indent (spaces, with tabs expanded)."""
    indent = 0
    for ch in line:
        if ch == " ":
            indent += 1
        elif ch == "\t":
            indent += tab_size
        else:
            break
    return indent


def parse_filename(filename: str) -> dict:
    """Parse `n_a_b_c.py` -> {sample_id, co_lines, completion_line, placeholder}.

    Field semantics (confirmed by user):
        n: sample_id (0..1199; 0..399=clean, 400..799=co_below, 800..1199=co_above)
        a: co_lines - 1 (true CO-code line count = a + 1; invalid for clean segment)
        b: completion_line (1-indexed)
        c: deprecated placeholder (= a + 1 + b for non-clean), ignore
    """
    base = filename
    if base.endswith(".py"):
        base = base[:-3]
    parts = base.split("_")
    if len(parts) < 4:
        raise ValueError(f"Bad filename format: {filename}")
    return {
        "sample_id": int(parts[0]),
        "co_lines": int(parts[1]) + 1,
        "completion_line": int(parts[2]),
        "placeholder": int(parts[3]),
    }


def load_yaml(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def deep_merge(base: dict, override: dict) -> dict:
    """Recursive dict merge — override wins."""
    out = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_full_config(
    base_path: str | Path,
    model_path: str | Path,
    ablation_path: str | Path,
) -> dict:
    """Compose base + model + ablation YAMLs into one config dict."""
    cfg = load_yaml(base_path)
    cfg = deep_merge(cfg, {"model": load_yaml(model_path)})
    cfg = deep_merge(cfg, {"ablation": load_yaml(ablation_path)})
    return cfg


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def jsonl_iter(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def jsonl_dump(records, path: str | Path) -> None:
    ensure_dir(Path(path).parent)
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def safe_clean_dir(path: str | Path) -> None:
    """Empty a directory while keeping the directory itself."""
    p = Path(path)
    if not p.exists():
        return
    for entry in p.iterdir():
        if entry.is_file() or entry.is_symlink():
            entry.unlink()
        elif entry.is_dir():
            import shutil
            shutil.rmtree(entry)


def find_file_for_sample_id(directory: str | Path, sample_id: int) -> Path | None:
    """Find the unique file in `directory` whose first underscore-segment == sample_id."""
    prefix = f"{sample_id}_"
    d = Path(directory)
    for p in d.iterdir():
        if p.name.startswith(prefix):
            return p
    return None
