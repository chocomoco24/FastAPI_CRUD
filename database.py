from models import Product
import db_models
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine


db_url = "postgresql://postgres:agartala@localhost:5432/fastapi"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    db_models.Base.metadata.create_all(bind=engine)
    
    db = session()
    try:
        count = db.query(db_models.Product).count()
        if count > 0:
            print("----- Database already initialized -----")
            return
        
        print("----- Creating Database Tables -----")
        print(".\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n")
        for product in products:
            db.add(db_models.Product(**product.model_dump()))
        db.commit()
        print("----- Database initialized successfully -----")
        return 
    finally:
        db.close()