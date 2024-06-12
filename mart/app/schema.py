from sqlmodel import SQLModel, Field
from typing import Literal

class Product(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    name: str
    # category: Literal["Food", "Health", "Fashion", "Electronics", "Sports", "Vahicle", "Furniture", "Literature"]
    price: int
    quantity : int

class AddProduct(SQLModel):
    name: str
    # category: Literal["Food", "Health", "Fashion", "Electronics", "Sports", "Vahicle", "Furniture", "Literature"]
    price: int
    quantity : int


class UpdateProduct(SQLModel):
    name: None| str = Field(None)
    # category: None| Literal["Food", "Health", "Fashion", "Electronics", "Sports", "Vahicle", "Furniture", "Literature"]
    price: None| int = Field(None)
    quantity : None| int = Field(None)

