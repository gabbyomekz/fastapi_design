from datetime import datetime, time, timedelta
from enum import Enum
from typing import Literal, Union
from uuid import UUID

from fastapi import Body, FastAPI, Query, Path, Cookie, Header, status, Form
from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()

# form data in fastapi

@app.post("/login/")
async def login(username: str = Form(...), password: str = Body(...)):
    print("password", password)
    return {"username": username}

@app.post("/login-json/")
async def login_json(username: str = Body(...), password: str = Body(...)):
    print("password", password)
    return {"username": username}
