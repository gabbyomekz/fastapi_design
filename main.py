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
)
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from starlette.responses import HTMLResponse

app = FastAPI()

# request forms and files in fastapi

@app.post("/files/")
async def create_file(
    file: bytes = File(...),
    another_file: UploadFile = File(...),
    token: str = Form(...),
    hi: str = Body(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "another_file_content_type": another_file.content_type,
        "hi": hi
    }
