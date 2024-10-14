
from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal
from uuid import UUID

from fastapi import Body, FastAPI, Query, Path, Cookie, Header
from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()

# Part 13 - Response Model in fastapi

class FoodItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

food_items = {
    "milk": {"name": "Milk", "price": 20.5},
    "chicken": {"name": "Chicken", "description": "rich in protein, good for athletes", "price": 45, "tax": 4.7},
    "fruits": {"name": "Fruits", "description": None, "price": 35.6, "tax": 3.27, "tags": []},
}

@app.get("/food_items/{food_item_id}", response_model=FoodItem, response_model_exclude_unset=True)
async def read_food_item(food_item_id: Literal["milk", "chicken", "fruits"]):
    return food_items[food_item_id]

@app.post("/food_items/", response_model=FoodItem)
async def create_food_item(food_item: FoodItem):
    return food_item

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


@app.get(
    "/food_items/{food_item_id}/name",
    response_model=FoodItem,
    response_model_include={"name", "description"},
)
async def read_food_item_name(food_item_id: Literal["foo", "bar", "baz"]):
    return food_items[food_item_id]


@app.get("/food_items/{food_item_id}/public", response_model=FoodItem, response_model_exclude={"tax"})
async def read_items_public_data(food_item_id: Literal["milk", "chicken", "fruits"]):
    return food_items[food_item_id]
