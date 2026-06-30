from fastapi import FastAPI

from .config import settings

app = FastAPI()


@app.get("/info")
async def info():

