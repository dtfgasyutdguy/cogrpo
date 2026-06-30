from fastapi import FastAPI

app = FastAPI()

items = {}


@app.on_event("startup")
async def startup_event():
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}

# async def read_items(item_id: str):

@app.get("/items/{item_id}")

    return items[item_id]
