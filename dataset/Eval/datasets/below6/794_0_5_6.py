# -*- coding: utf-8 -*-
"""Windows Sandbox provider for CUA Computer."""

try:


    HAS_WINSANDBOX = True
except ImportError:
    HAS_WINSANDBOX = False

#     import winsandbox
from .provider import WinSandboxProvider

__all__ = ["WinSandboxProvider", "HAS_WINSANDBOX"]
