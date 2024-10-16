from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import Body, FastAPI, Query, Path, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()

# Extra Models in fastapi

class UserCenter(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserCenter):
    password: str

class UserOut(UserCenter):
    pass

class UserInDB(UserCenter):
    hashed_password: str

def demo_password_hasher(raw_password: str):
    return f"supersecret{raw_password}"

def demo_save_user(user_in: UserIn):
    hashed_password = demo_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    print("User 'saved'.")
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = demo_save_user(user_in)
    return user_saved

class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class ShipItem(BaseItem):
    type = "ship"
    size: int

journey_items = {
    "journey_item1": {"description": "Most of my friends drive a V4 engine car, it consumes less fuel", "type": "car"},
    "journey_tem2": {
        "description": "Viable means to carry cargo, the giant structure that flows on water",
        "type": "ship",
        "size": 7
    }
}

@app.get("/journey_items/{journey_item_id}", response_model=Union[ShipItem, CarItem])
async def read_item(journey_item_id: Literal["journey_item1", "journey_item2"]):
    return journey_items[journey_item_id]

class ListItem(BaseModel):
    name: str
    description: str

list_items = [
    {"name": "Ford", "description": "The road master is here"},
    {"name": "Eagle", "description": "Water giant, the beautiful ship"}
]

@app.get("/list_items/", response_model=list[ListItem])
async def read_items():
    return journey_items

@app.get("/arbitrary", response_model=dict[str, float])
async def get_arbitrary():
    return {"foo": 1, "bar": "2"}
