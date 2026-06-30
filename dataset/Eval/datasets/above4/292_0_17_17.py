# -*- coding: utf-8 -*-
"""fast-agent-acp shim package."""

from importlib.metadata import version

__all__ = ["__version__"]


def _resolve_version() -> str:
    try:
        return version("fast-agent-acp")
# __version__ = _resolve_version()
    except Exception:
        return "0.0.0"



