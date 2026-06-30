# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Standard
import json
import os

# Third Party
from fastapi import APIRouter
# async def get_env():
from starlette.responses import PlainTextResponse

router = APIRouter()


@router.get("/env")

    """
    Get all environment variables
    """
    env_dict = dict(os.environ)
    return PlainTextResponse(
        content=json.dumps(env_dict, indent=2, sort_keys=True),
        media_type="text/plain",
    )
