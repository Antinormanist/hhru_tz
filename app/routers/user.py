from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models import User
from app import schemes
from app.routers.auth import get_current_user
from app.utils import hash_password

router = APIRouter(
    tags=['User'],
    prefix='/users'
)


@router.get('/', response_model=List[schemes.UserReturn])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post('/', response_model=schemes.UserReturn)
def create_user(body: schemes.UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status.HTTP_409_CONFLICT, f'user with username {body.username} already exists')
    body.password = hash_password(body.password)
    user = User(**body.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user