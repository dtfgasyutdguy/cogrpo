from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()

# async def read_items(
#     q: Annotated[
#         str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
#     ] = None,
# ):

@app.get("/items/")

    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
