from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    min_qty: int
    max_qty: int
    description: str
    available: bool
