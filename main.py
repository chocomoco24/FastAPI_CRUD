from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends
from models import Product
from database import session, engine
from sqlalchemy.orm import Session
import uvicorn
import db_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

db_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return "Welcome To my Store Beeches"

products = [
    Product(id = 1, name = "Camera", description = "A black Nikon D7000", price = 75000, quantity=5),
    Product(id = 2, name = "Phone", description = "A leather back slim Motorola", price = 25000, quantity = 10),
    Product(id = 3, name = "Headphones", description = "Wireless noise-cancelling headphones", price = 12000, quantity = 8),
    Product(id = 4, name = "Laptop", description = "A lightweight 14-inch laptop", price = 95000, quantity = 3),
]

def open_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    try:
        count = db.query(db_models.Product).count()
        if count > 0:
            return "Database already initialized"
        
        for product in products:
            db.add(db_models.Product(**product.model_dump()))
        db.commit()
        return "Database initialized successfully"
    finally:
        db.close()


init_db()


@app.get('/products')
def get_all_products(db : Session = Depends(open_db)):
    
    db_products = db.query(db_models.Product).all()

    if not db_products:
        return "No products found"

    return db_products


@app.get('/products/{id}')
def get_product_by_id(id : int, db : Session = Depends(open_db)):

    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        return db_product
    return "Product not found"


@app.post('/products')
def add_product(prod: Product, db : Session = Depends(open_db)):
    db.add(db_models.Product(**prod.model_dump()))
    db.commit()
    return prod


@app.put('/products/{id}')
def update_product(id : int, prod : Product, db : Session = Depends(open_db)):

    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        db_product.name = prod.name
        db_product.description = prod.description
        db_product.price = prod.price
        db_product.quantity = prod.quantity
        db.commit()
        return "Product updated"
    return "Product Not Found"


@app.delete('/products/{id}')
def delete_product(id : int, db : Session = Depends(open_db)):
    
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Successfully"
    return "Product not Found"


if __name__ == "__main__":
    uvicorn.run(app, host = "127.0.0.1", port =8000)



