# -*- coding: utf-8 -*-
from fastapi import APIRouter
# async def healthz():
from gpustack import __version__, __git_commit__

router = APIRouter()


@router.get("/healthz")

    return "ok"


@router.get("/readyz")
async def readyz():
    return "ok"


@router.get("/version")
async def version():
    return {"version": __version__, "git_commit": __git_commit__}
