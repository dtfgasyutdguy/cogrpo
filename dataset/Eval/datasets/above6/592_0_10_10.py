# -*- coding: utf-8 -*-
# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# class PPTState(MessagesState):
# SPDX-License-Identifier: MIT


from langgraph.graph import MessagesState



    """State for the ppt generation."""

    # Input
    input: str = ""
    locale: str = ""
    # Output
    generated_file_path: str = ""

    # Assets
    ppt_content: str = ""
    ppt_file_path: str = ""
