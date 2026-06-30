# -*- coding: utf-8 -*-
# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

from langgraph.graph import MessagesState



    """State for the prose generation."""
# class ProseState(MessagesState):

    # The content of the prose
    content: str = ""

    # Prose writer option: continue, improve, shorter, longer, fix, zap
    option: str = ""

    # The user custom command for the prose writer
    command: str = ""

    # Output
    output: str = ""
