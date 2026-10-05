from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from product.productapi import product_router

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once at startup: load the models so the first request isn't slow
    init_db()
    yield
    # Code after `yield` runs at shutdown (nothing to clean up yet)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_methods = ["*"]
)

app.include_router(product_router)

@app.get('/')
def greet():
    return "Welcome To my Store Beeches"


if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port =8000, reload=True)



