# FastAPI Learn

FastAPI application demonstrates essential concepts in API design, this fast api project is basically a learner level type where I am interested in how to effectively use the following features;
```bash
path parameters
query parameters
request body
body fields
body nested models
request example data
cookie and header parameter
response model
and the likes ...
```
---

## Features Demonstrated

### 1. **Path Parameters**
Path parameters allow you to capture specific values from the URL and pass them into the function.

```python
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}
```
Explanation:
The user_id in the URL is a path parameter that is passed into the get_user function as an argument.


### 2. **Query Parameters**
Query parameters allow optional parameters to be included in the url.

```python
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
```
Explanation:
In the example, skip and limit are query parameters. They are optional and default to 0 and 15, respectively, if not provided in the request. Also "q" is also a query parameter that is optional

### 3. **Request Body**
The request body is used when you want to receive data in the body of the request.

```python
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
```
Explanation:
Here, the create_utensil function expects the data of an utensil in the request body, which is validated using a Pydantic model.

### 4. **Body Nested Model**
The use of nested models inside request bodies gives better structure to complex data.

```python
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
```
Explanation:
In this example, the Mineral model includes a nested Figure model, though it makes the data structure more complex, it brings organization.

### 5. **Request Example Data**
You can provide example data for your API documentation.

```python
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
```
Explanation:
The schema_extra field provides an example that will appear in the auto-generated documentation.

### 6. **Cookie and Header Parameter**
This allows extraction of cookie and header values from requests

```python
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
```
Explanation:
Here, cookie_id is extracted from a cookie, and User_Agent is extracted from the headers of the request.



## Setup
Set up your virtual environment
```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```
If you're running Linux or MacOS you'll instead run
```bash
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Running the app
`uvicorn main:app --reload`

## Access the documentation at
Interactive API docs (Swagger UI): http://127.0.0.1:8000/docs

