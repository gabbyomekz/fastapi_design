from enum import Enum
from fastapi import FastAPI

app = FastAPI()

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
