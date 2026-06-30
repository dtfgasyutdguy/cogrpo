from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: str | None = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None,
):
    if not q:
        return last_query
    return q

# async def read_query(
#     query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
# ):

@app.get("/items/")

    return {"q_or_cookie": query_or_default}
