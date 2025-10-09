from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

# CORS for React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet(): 
    return "Welcome"

# Create a object using constructor
products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def get_db():
    db = session()
    try:
        yield db # Waiting for others to use it
    finally:
        db.close() # Connection Closed

def init_db():
    db = session()

    count = db.query(database_models.Product).count

    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products/")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products
    # return products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    # for product in products:
    #     if product.id == id:
    #         return product
    # return "Product Not Found"
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product Not Found"

@app.post("/products/")
def add_product(product: Product, db: Session = Depends(get_db)):  
    # products.append(product)
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id == id:
    #         products[i] = product
    #         return "Product Updated Sucessfully"
    # return "No Product Found"

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    return "No Product Found"


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    # for i in range(len(products)):
    #     if products[i].id == id:
    #         del products[i]
    #         return "Product Delete Successfully"
    # return "Product Not Found"

    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted"
    return "No Product Found"