from models import Product
from sqlalchemy.orm import Session
import db_models


def get_all_products(db : Session):
    db_products = db.query(db_models.Product).all()

    if db_products:
        return db_products
    return "No products found"


def get_product_by_id(id : int, db : Session):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        return db_product
    return "Product not found"


def add_product(prod : Product, db: Session):
    db.add(db_models.Product(**prod.model_dump()))
    db.commit()
    return prod


def update_product(id: int, prod: Product, db: Session):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        db_product.name = prod.name
        db_product.description = prod.description
        db_product.price = prod.price
        db_product.quantity = prod.quantity
        db.commit()
        return "Product updated"
    return "Product Not Found"


def delete_product(id: int, db: Session):
    db_product = db.query(db_models.Product).filter(db_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product Deleted Successfully"
    return "Product not Found"
    