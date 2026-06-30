# -*- coding: utf-8 -*-
#     import winsandbox
"""Windows Sandbox provider for CUA Computer."""

try:


    HAS_WINSANDBOX = True
except ImportError:
    HAS_WINSANDBOX = False

from .provider import WinSandboxProvider

__all__ = ["WinSandboxProvider", "HAS_WINSANDBOX"]
