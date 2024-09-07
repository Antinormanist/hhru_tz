from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models import Product, User, Category
from app import schemes
from app.routers.auth import get_current_user

router = APIRouter(
    tags=['Product'],
    prefix='/products'
)


@router.get('/', response_model=List[schemes.ProductReturn])
def get_products(create_asc: bool = False, create_desc: bool = False, price_asc: bool = False, price_desc: bool = False, search: str = '', db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.icontains(search))
    if create_asc:
        products = products.order_by(Product.created_at)
    if create_desc:
        products = products.order_by(Product.created_at.desc())
    if price_asc:
        products = products.order_by(Product.price)
    if price_desc:
        products = products.order_by(Product.price.desc())
    return products


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemes.ProductReturn)
def create_product(body: schemes.ProductCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if db.query(User).filter(User.id == body.owner_id).first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'user with id {body.owner_id} is not found')
    if db.query(Category).filter(Category.id == body.category_id).first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'category with id {body.category_id} is not found')
    product = Product(**body.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put('/{id}', response_model=schemes.ProductReturn)
def full_update_product(id: int, body: schemes.ProductFullUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if db.query(User).filter(User.id == body.owner_id).first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'user with id {body.owner_id} is not found')
    if db.query(Category).filter(Category.id == body.category_id).first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'category with id {body.category_id} is not found')
    product = db.query(Product).filter(Product.id == id)
    if product.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'product with id {id} is not found')
    if product.first().owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'product with id {id} is not your product')
    product.update(body.dict(), synchronize_session=False)
    db.commit()
    db.refresh(product.first())
    return product.first()


@router.patch('/{id}', response_model=schemes.ProductReturn)
def partial_update_product(id: int, body: schemes.ProductPartialUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if body.owner_id and db.query(User).filter(User.id == body.owner_id).first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'user with id {body.owner_id} is not found')
    if body.category_id and db.query(Category).filter(Category.id == body.category_id).first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'category with id {body.category_id} is not found')
    product = db.query(Product).filter(Product.id == id)
    if product.first() is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'product with id {id} is not found')
    if product.first().owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'product with id {id} is not your product')
    product = product.first()
    for field, value in body.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == id).first()
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f'product with id {id} is not found')
    if product.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'product with id {id} is not your product')
    db.delete(product)
    db.commit()
