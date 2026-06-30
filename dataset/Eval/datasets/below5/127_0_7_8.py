# -*- coding: utf-8 -*-
# Copyright (c) Microsoft. All rights reserved.

from .base import ExecutionStrategy



    """Placeholder strategy for future inter-process primitives.

    The class exists to reserve the `ipc` alias and make the planned
    implementation discoverable. Attempting to use it today will raise
# class InterProcessExecutionStrategy(ExecutionStrategy):
    `NotImplementedError` once the execution contract is finalized.
    """

    alias: str = "ipc"

    # TODO: to be implemented
