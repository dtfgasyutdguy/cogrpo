from __future__ import annotations

from typing import List

from .utils import count_visual_indent


SYS_CONTENT = """Based on the provided code context, generate only the missing Python code at the location marked with "# missing: N lines".

Notes:
Strictly return only those N lines of code, enclosed in a code block.
Do not repeat any existing code or context.
Do not include any explanations, comments, or extra text.
Ensure your completion matches the indentation of the surrounding code.

Example:
Input:
def calculate_sum(a, b):
    # missing: 1 line
    return s

Output:
```python
    s = a + b
```

Now complete the following context:
"""


def build_prompt_text(file_lines: List[str], completion_line: int, missing_lines: int) -> str:
    """Insert a `# missing: N lines` placeholder into raw file content.

    `completion_line` is 1-indexed (matches the dataset filename convention).
    `file_lines` already contains trailing newlines on each line.
    Returns the raw user-prompt content (without sysContent prefix).
    """
    if not file_lines:
        return ""

    # Indent matches the line BEFORE the completion (mirrors original code).
    ref_idx = completion_line - 2
    if ref_idx < 0:
        ref_idx = 0
    indent_str = " " * count_visual_indent(file_lines[ref_idx])

    # Insert "# missing: ..." at the completion line position, replacing the
    # original 1 line with the comment line.
    body = (
        "".join(file_lines[: completion_line - 1])
        + f"{indent_str}# missing: {missing_lines} line{'s' if missing_lines != 1 else ''}\n"
        + "".join(file_lines[completion_line:])
    )
    return body


def build_user_message(prompt_body: str) -> str:
    """Wrap the prompt body with the system instructions."""
    return SYS_CONTENT + "\n" + prompt_body


def build_chat_messages(prompt_body: str) -> List[dict]:
    """Format for chat-template tokenizers (Qwen / DeepSeek / CodeGemma instruct)."""
    return [{"role": "user", "content": build_user_message(prompt_body)}]
