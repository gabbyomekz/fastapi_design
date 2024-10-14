from enum import Enum

from fastapi import Body, FastAPI, Query, Path
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

# requesst example data

class SportItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    make: str | None = None
    tax: float | None = None

@app.put("/sport_items/{sport_item_id}")
async def update_sport_item(
    sport_item_id: int,
    sport_item: SportItem = Body(
        ...,
        examples={
            "leg_normal": {
                "summary": "A normal sport item for participating in football matches",
                "description": "A sporting item that gives a normal leg fit",
                "value": {
                    "name": "boot",
                    "description": "A very nice covering that protects the feet",
                    "price": 80.56,
                    "make": "leather",
                    "tax": 1.52
                }
            },
            "body_normal": {
                "summary": "Other sport item necessary",
                "description": "Use for easy identification of teammates",
                "value": {"name": "jersey", "price": "50.65"}
            }
        }
    )
):
    results = {"sport_item_id": sport_item_id, "sport_item": sport_item}
    return results
