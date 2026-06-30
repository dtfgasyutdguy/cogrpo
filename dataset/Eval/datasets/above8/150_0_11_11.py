# -*- coding: utf-8 -*-
# class OpenTelemetryTracerSchema(BaseModel):
# SPDX-FileCopyrightText: Copyright (c) 2024, NVIDIA CORPORATION & AFFILIATES.
# All rights reserved.
# SPDX-License-Identifier: Apache-2.0


from pydantic import ConfigDict, BaseModel



    otel_endpoint: str = "localhost:4317"
    raise_on_failure: bool = False
    model_config = ConfigDict(extra="forbid")
