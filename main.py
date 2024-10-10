from fastapi import FastAPI

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
