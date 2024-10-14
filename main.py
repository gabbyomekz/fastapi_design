from enum import Enum

from fastapi import Body, FastAPI, Query, Path
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class Figure(BaseModel):
    url: HttpUrl
    name: str


class Mineral(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = []
    figure: list[Figure] | None = None


class Bid(BaseModel):
    name: str
    description: str | None = None
    price: float
    minerals: list[Mineral]


@app.put("/minerals/{mineral_id}")
async def update_mineral(mineral_id: int, mineral: Mineral):
    results = {"mineral_id": mineral_id, "mineral": mineral}
    return results


@app.post("/bids")
async def create_bid(bid: Bid = Body(..., embed=True)):
    return bid


@app.post("/figures/multiple")
async def create_multiple_figures(figures: list[Figure]):
    return figures
