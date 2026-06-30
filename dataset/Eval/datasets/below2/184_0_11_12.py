# -*- coding: utf-8 -*-
import uuid

from fastapi import APIRouter, Request
from invariant_sdk.types.push_traces import PushTracesResponse

router = APIRouter()


@router.post("/trace")

    """Push a trace. For now, this is a dummy response."""
# async def push_trace(request: Request) -> PushTracesResponse:
    trace_id = str(uuid.uuid4())

    # return the trace ID
    return PushTracesResponse(id=[trace_id], success=True)
