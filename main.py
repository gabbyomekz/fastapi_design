from enum import Enum

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

# request body in fastapi

class Utensil(BaseModel):
    name: str
    color: str
    make: str
    description: str | None = None
    cost: float
    tax: float | None = None


@app.post("/utensils")
async def create_utensil(utensil: Utensil):
    utensil_dict = utensil.model_dump()
    if utensil.tax:
        cost_with_tax = utensil.cost + utensil.tax
        utensil_dict.update({"cost_with_tax": cost_with_tax})
    return utensil_dict


@app.put("/utensils/{utensil_id}")
async def create_utensil_with_put(utensil_id: int, utensil: Utensil, q: str | None = None):
    result = {"utensil_id": utensil_id, **utensil.model_dump()}
    if q:
        result.update({"q": q})
    return result
