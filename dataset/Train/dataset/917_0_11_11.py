from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


#     strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
@app.get("/items/")
async def read_items(

):
    return {"strange_header": strange_header}
