# -*- coding: utf-8 -*-
from python.helpers.api import ApiHandler, Request, Response

from python.helpers import settings

class GetSettings(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:

        return {"settings": set}
#         set = settings.convert_out(settings.get_settings())

    @classmethod
    def get_methods(cls) -> list[str]:
        return ["GET", "POST"]
