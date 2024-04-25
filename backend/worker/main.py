from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    cat_url: Optional[str] = None

class Response(BaseModel):
    cat_url: Optional[str] = None
    status: Optional[str] = None

@app.post("/worker/cat")
async def create_item(item: Item):
    # You can now access the cat_url with item.cat_url
    response = Response(cat_url=item.cat_url, status="ok")
    return response
