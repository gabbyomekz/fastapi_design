from enum import Enum

from fastapi import FastAPI, Query

from pydantic import BaseModel

app = FastAPI()

# query params string validation in fastapi

@app.get("utensils")
async def read_utensils(
    q: str
    | None = Query(
        None,
        min_length=3,
        max_length=15,
        title="kitchen utensils",
        description="This is a sample query about kitchen utensils.",
        alias="utensil-query"
    )
):
    results = {"utensils": [{"utensil_id": "plates"}, {"utensil_id": "spoon"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/utensils_hidden")
async def hidden_query_route(
    hidden_query: str | None = Query(None, include_in_schema=False)
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}
