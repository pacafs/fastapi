from enum import Enum, nonmember

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"

class Item(BaseModel):
    id: int
    name: str
    price: float
    count: int
    category: Category


items = {
    1: Item(id=1, name="Drill", price=89.99, count=15, category=Category.TOOLS),
    2: Item(id=2, name="Hammer", price=19.99, count=50, category=Category.TOOLS),
    3: Item(id=3, name="Screwdriver Set", price=29.99, count=25, category=Category.TOOLS),  
    4: Item(id=4, name="Wood Glue", price=5.99, count=100, category=Category.CONSUMABLES),
    5: Item(id=5, name="Sandpaper Pack", price=12.49, count=75, category=Category.CONSUMABLES),
    6: Item(id=6, name="Paint Brushes", price=15.99, count=40, category=Category.CONSUMABLES),
    7: Item(id=7, name="Safety Goggles", price=9.99, count=30, category=Category.CONSUMABLES)
}

Selection = dict[
    str,str | int | float | Category | None
] # dict containing the user's query arguments

# FastAPI handles JSON serialization and deserialization for you.
# We can simply use built-in python and Pydantic types, in this case, a dict[int, Item].

@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"Items: ": items}

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(
            status_code=404,detail=f"Item with {item_id} doest exist!"
        )
    return items[item_id]

@app.get("/items/")
def query_item_by_parameters(id: int | None = None, name: str | None = None, price: float | None = None, count: int | None = None, category: Category | None = None) -> dict[str, dict[int, Item]]:
    def check_item(item: Item) -> bool:
        return all(
            (
                id is None or item.id == id,
                name is None or name in item.name.lower(),
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category == category
            )
        )
    selection = {item.id: item for item in items.values() if check_item(item)}
    return {
        "Items": selection
    }
