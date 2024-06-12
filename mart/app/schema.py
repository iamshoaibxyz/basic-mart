from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    id: int | None = Field(None, primary_key=True)
    name: str
    category: str = Field(default='food | health | fashion | electronics | sports | vahicle | furniture | literature | other')
    price: int
    quantity : int

class UpdateProduct(SQLModel):
    name: None| str = Field(None)
    category: None| str = Field(default='food | health | fashion | electronics | sports | vahicle | furniture | literature | other')
    price: None| int = Field(None)
    quantity : None| int = Field(None)

