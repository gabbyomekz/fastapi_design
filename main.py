from enum import Enum
from fastapi import FastAPI

app = FastAPI()

# query parameters in fastapi

cook_utensils_db = [{"utensil_name": "plates"}, {"utensil_name": "spoon"}, {"utensil_name": "fork"}]


@app.get("/utensils")
async def list_utensils(skip: int = 0, limit: int = 15):
    return cook_utensils_db[skip: skip + limit]


@app.get("/utensils/{utensil_id}")
async def get_utensil(
    utensil_id: str, sample_query_param: str, q: str | None = None, short: bool = False
):
    utensil = {"utensil_id": utensil_id, "sample_query_param": sample_query_param}
    if q:
        utensil.update({"q": q})
    if not short:
        utensil.update(
            {
                "description": "Utensils are very essential in the kitchen, can as well be dangerous"
            }
        )
    return utensil


@app.get("/users/{user_id}/utensils/{utensil_id}")
async def get_user_utensil(
    user_id: int, utensil_id: str, q: str | None = None, short: bool = False
):
    utensil = {"utensil_id": utensil_id, "owner_id": user_id}
    if q:
        utensil.update({"q": q})
    if not short:
        utensil.update(
            {
                "description": "Utensils are very essential in the kitchen, can as well be dangerous"
            }
        )
    return utensil
