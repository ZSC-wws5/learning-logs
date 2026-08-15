from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message" : "Hello World,Hello FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id : int, q : str | None = None):
    return {"item_id" : item_id, "q": q}