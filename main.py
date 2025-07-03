from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from scrapers import ScrapCompiler

from models.AllCoursesRequest import AllCoursesRequest

app = FastAPI()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Golf API"}

@app.post("/courses")
async def getAllCourses(request: AllCoursesRequest):
    dataRecieved = request.model_dump()
    return dataRecieved


# # Get item by ID
# @app.get("/items/{item_id}")
# async def get_item(item_id: int):
#     item = next((item for item in items if item["id"] == item_id), None)
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item

# # Add a new item
# @app.post("/items")
# async def add_item(item: Item):
#     # Check if id already exists
#     if any(existing_item["id"] == item.id for existing_item in items):
#         raise HTTPException(status_code=400, detail="Item with this ID already exists")
#     items.append(item.dict())
#     return item

# # Update an existing item
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, updated_item: Item):
#     for index, existing_item in enumerate(items):
#         if existing_item["id"] == item_id:
#             items[index] = updated_item.dict()
#             return updated_item
#     raise HTTPException(status_code=404, detail="Item not found")

# # Delete an item
# @app.delete("/items/{item_id}")
# async def delete_item(item_id: int):
#     for index, existing_item in enumerate(items):
#         if existing_item["id"] == item_id:
#             deleted_item = items.pop(index)
#             return {"message": f"Deleted item with id {item_id}"}
#     raise HTTPException(status_code=404, detail="Item not found")
