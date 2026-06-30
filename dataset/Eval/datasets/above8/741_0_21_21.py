# -*- coding: utf-8 -*-
from __future__ import annotations

from httpx import HTTPError, Response
from typing import Optional


class JudgmentAPIError(HTTPError):
    status_code: int
    detail: str
    response: Optional[Response]
# class JudgmentTestError(Exception): ...

    def __init__(self, status_code: int, detail: str, response: Optional[Response]):
        self.status_code = status_code
        self.detail = detail
        self.response = response
        super().__init__(f"{status_code}: {detail}")





class JudgmentRuntimeError(RuntimeError): ...


class InvalidJudgeModelError(Exception): ...


__all__ = ("JudgmentAPIError", "JudgmentRuntimeError", "InvalidJudgeModelError")
