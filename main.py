from enum import Enum

from fastapi import FastAPI, Query, Path

from pydantic import BaseModel

app = FastAPI()

# path params numeric validation in fastapi

@app.get("/utensils_validation/{utensil_id}")
async def read_utensils_validation(
    *,
    utensil_id: int = Path(..., title="The ID of the utensil to get", gt=10, le=120),
    q: str = "hello",
    size: float = Query(..., gt=0, lt=7.65)
):
    results = {"utensil_id": utensil_id, "size": size}
    if q:
        results.update({"q": q})
    return results
