from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models import Category
from app import schemes
from app.routers.auth import get_current_user

router = APIRouter(
    tags=['Category'],
    prefix='/categories'
)


@router.get('/', response_model=List[schemes.CategoryReturn])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemes.CategoryReturn)
def create_category(body: schemes.CategoryCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if db.query(Category).filter(Category.name == body.name).first():
        raise HTTPException(status.HTTP_409_CONFLICT, f'category with name {body.name} already exists')
    category = Category(**body.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category