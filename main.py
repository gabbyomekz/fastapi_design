from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import (
    Body,
    FastAPI,
    Query,
    Path,
    Cookie,
    Header,
    status,
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import HTMLResponse

app = FastAPI()

# path operation configuration

class FashionItem(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

class Tags(Enum):
    fashion_items = "fashion_items"
    fashion_users = "fashion_users"

@app.post(
    "/fashion_items/",
    response_model=FashionItem,
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.fashion_items],
    summary="Things in the fashion world that excites you",
    description="Leather shoe",
    # "name; description; price; tax; and a set of "
    # "unique tags",
    response_description="Hand made with comfy base"
)
async def create_fashion_item(fashion_item: FashionItem):
    """
    Create a fashion item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return fashion_item

@app.get("/fashion_items/", tags=[Tags.fashion_items])
async def read_fashion_items():
    return [{"name": "Leather Shoe", "price": 55}]

@app.get("/fashion_users/", tags=[Tags.fashion_users])
async def read_fashion_users():
    return [{"username": "GlowUpDesigners"}]

@app.get("/elements/", tags=[Tags.fashion_items], deprecated=True)
async def read_elements():
    return [{"fashion_item_id": "Leather Shoe"}]
