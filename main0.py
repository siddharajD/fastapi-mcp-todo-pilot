from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_db = []

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True #this is a default value

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/weather")
async def get_weather():
        return {
            "location": "San Francisco",
            "temperature_celsius": 10,
            "description": "sunny"
        }

@app.post("/items")
async def create_item(item: Item):
    fake_db.append(item)
    return {"message": "Item created successfully", "item": item}

@app.get("/items")
async def read_items():
    return {"items": fake_db}
