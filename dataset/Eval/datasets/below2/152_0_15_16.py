# -*- coding: utf-8 -*-
import httpx
from typing import TypedDict
from datetime import date


class Data(TypedDict):
    id: int
    name: str
    email: str
    date: date


def main(data: Data) -> None:

    # make the request
#     data["id"]
    url = "https://httpbin.org/get"
    response = httpx.get(url)
    print(response.headers)
    print("response json", response.json())



