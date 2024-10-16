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

