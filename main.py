from datetime import datetime, time, timedelta

from enum import Enum
from uuid import UUID

from fastapi import Body, FastAPI, Query, Path, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

# the basic way towards routing a fastapi using ("GET", "POST", "PUT")

@app.get("/")
async def root():
    return {"message": "locked on fastapi world"}

@app.post("/")
async def post():
    return {"message": "fastapi world from the post route"}

@app.put("/")
async def put():
    return {"message": "fastapi world from the put route"}

# path parameters in fastapi

@app.get("/users")
async def list_users():
    return {"message": "list users route"}

@app.get("/users/me")
async def get_current_user():
    return {"Message": "this is the current user"}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}

class vehicleEnum(str, Enum):
    car = "car"
    bus = "bus"
    train = "train"


@app.get("/vehicles/{vehicle_name}")
async def get_vehicle(vehicle_name: vehicleEnum):
    if vehicle_name == vehicleEnum.bus:
        return {"vehicle_name": vehicle_name, "message": "commercial use, medium sized for short travels"}

    if vehicle_name.value == "car":
        return {
            "vehicle_name": vehicle_name, "message": "personal use, small sized for family convenience"}
    return {"vehicle_name": vehicle_name, "message": "commercial use, large sized for long distance travels"}

# query parameters in fastapi

cook_utensils_db = [{"utensil_name": "plates"}, {"utensil_name": "spoon"}, {"utensil_name": "fork"}]

@app.get("/old_utensils")
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

# query params string validation in fastapi

@app.get("/utensils")
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

# body nested models in fastapi

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

# requesst example data in fastapi

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

# Extra Data Types in fastapi

@app.put("/sport_items/{sport_item_id}")
async def read_sport_items(
    sport_item_id: UUID,
    start_date: datetime | None = Body(None),
    end_date: datetime | None = Body(None),
    repeat_at: time | None = Body(None),
    process_after: timedelta | None = Body(None)
):
    start_process = start_date + process_after
    duration = end_date - start_process
    return {
        "sport_item_id": sport_item_id,
        "start_date": start_date,
        "end_date": end_date,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration
    }

# Cookie and Header Parameters in fastapi

@app.get("/sport_items")
async def read_sport_items(
    cookie_id: str | None = Cookie(None),
    accept_encoding: str | None = Header(None),
    sec_ch_ua: str | None = Header(None),
    user_agent: str | None = Header(None),
    x_token: list[str] | None = Header(None),
):
    return {
        "cookie_id": cookie_id,
        "Accept-Encoding": accept_encoding,
        "sec-ch-ua": sec_ch_ua,
        "User-Agent": user_agent,
        "X-Token values": x_token,
    }
