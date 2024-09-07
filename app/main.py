from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, user, category, product

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(category.router)
app.include_router(product.router)
