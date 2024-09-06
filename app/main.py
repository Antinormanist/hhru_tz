from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)

@app.get('/')
def index():
    return {'message': 'Hello world!'}
