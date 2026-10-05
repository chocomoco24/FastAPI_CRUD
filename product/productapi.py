from fastapi import APIRouter
import controllers
from fastapi import Depends
from sqlalchemy.orm import Session
from models import Product
from database import open_db


product_router = APIRouter(prefix='/products')

@product_router.get('/product')
def get_all_products(db : Session = Depends(open_db)):
    return controllers.get_all_products(db)

@product_router.post('/product')
def add_product(prod: Product, db : Session = Depends(open_db)):
    return controllers.add_product(prod, db)

@product_router.get('/{id}')
def get_product_by_id(id : int, db : Session = Depends(open_db)):
    return controllers.get_product_by_id(id, db)

@product_router.put('/{id}')
def update_product(id : int, prod : Product, db : Session = Depends(open_db)):
    return controllers.update_product(id, prod, db)

@product_router.delete('/{id}')
def delete_product(id : int, db : Session = Depends(open_db)):
    return controllers.delete_product(id, db) 

