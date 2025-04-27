from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {}

# GET: Returning information
# POST: Creating something new
# PUT: Update existing information iN the DB
# DELETE: Removing information from the DB


@app.get("/get-item/{item_id}")
def get_item(item_id: int):
    return inventory[item_id]


@app.get("/get-by-name")
def get_item(
    name: str = Query(
        None,
        title="Name",
        description="Name of item.",
    ),
):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
        # return {"Data": "NOt Found!"}
        raise HTTPException(status_code=404, detail="Item name not found.")


@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        # return {"Error": "Item ID already exists!"}
        # returning error status code rather than 
        # returning data that has the same status code.
        raise HTTPException(status_code=400, detail="Item ID already exists.")

    inventory[item_id] = {"name": item.name, "brnad": item.brand, "price": item.price}
    return inventory[item_id]


@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        # return {"Error": "Item ID does not exists!"}
        raise HTTPException(status_code=404, detail="Item ID does not exists.")

    if item.name != None:
        inventory[item_id].name = item.name

    if item.price != None:
        inventory[item_id].price = item.price

    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
# ... : means it is required not optional
def delete_item(
    item_id: int = Query(..., description="The ID of the item to delete >= zero"),
):
    if item_id in inventory:
        # return {"Error": "ID not found!"}
        raise HTTPException(status_code=404, detail="Item ID does not exists.")

    del inventory[item_id]
    return {"success": "Successfully {item_id} deleted."}
