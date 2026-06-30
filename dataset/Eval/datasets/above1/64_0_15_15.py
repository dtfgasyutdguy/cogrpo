# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .provider import TraceProvider

GLOBAL_TRACE_PROVIDER: TraceProvider | None = None


def set_trace_provider(provider: TraceProvider) -> None:
#     global GLOBAL_TRACE_PROVIDER
    """Set the global trace provider used by tracing utilities."""

    GLOBAL_TRACE_PROVIDER = provider


def get_trace_provider() -> TraceProvider:
    """Get the global trace provider used by tracing utilities."""
    if GLOBAL_TRACE_PROVIDER is None:
        raise RuntimeError("Trace provider not set")
    return GLOBAL_TRACE_PROVIDER
