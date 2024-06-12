from fastapi import FastAPI, HTTPException, Depends
from app import setting
from app.schema import Product, AddProduct, UpdateProduct
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated

connection_str = str(setting.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(connection_str)

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Creating table")
    # SQLModel.metadata.create_all(engine)
    print("table created")
    yield

app: FastAPI = FastAPI(lifespan=lifespan, title="Basic Mart", servers=[{
    "url": "http://127.0.0.1:8000",
    "description": "Development server"
}])

# if category not in allowed_categories:
#             raise ValueError(f"Invalid category. Must be one of {', '.join(allowed_categories)}")
#         return category
# app: FastAPI = FastAPI(title="Basic Mart", servers=[{
#     "url": "http://127.0.0.1:8000",
#     "description": "Development server"
# }])

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def root():
    return {"message":"Mart api class"}

@app.post("/add-product", response_model=Product)
def add_product(product: Product, session: Annotated[Session, Depends(get_session) ] ):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.patch("/increment_product_items/${product_id}")
def update_product(product_id: int, add_item: int, session: Annotated[Session, Depends(get_session) ] ):
    db_product = session.exec(select(Product).where(Product.id==int(product_id))).first() #get(Product, int(product_id))
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    db_product.quantity += int(add_item)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.patch("/update_product/${product_id}")
def update_product(product_id: int, product: UpdateProduct, session: Annotated[Session, Depends(get_session) ] ):
    db_product = session.exec(select(Product).where(Product.id==int(product_id))).first() #get(Product, int(product_id))
    if not db_product:
        raise HTTPException(status_code=404, detail="product not found")
    updated_product = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(updated_product) 
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.get("/all-products", response_model=list[Product])
def add_product(session: Annotated[Session, Depends(get_session) ] ):
    products = session.exec(select(Product)).all()
    return products


@app.get("/get-product", response_model=Product)
def add_product(product_id: int, session: Annotated[Session, Depends(get_session) ] ):
    product = session.exec(select(Product).where(Product.id==int(product_id))).first()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product






# @app.patch("/heroes/{hero_id}", response_model=HeroRead)
# def update_hero(hero_id: int, hero: HeroUpdate):
#     with Session(engine) as session:
#         db_hero = session.get(Hero, hero_id)
#         if not db_hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         hero_data = hero.model_dump(exclude_unset=True)
#         db_hero.sqlmodel_update(hero_data)
#         session.add(db_hero)
#         session.commit()
#         session.refresh(db_hero)
#         return db_hero

