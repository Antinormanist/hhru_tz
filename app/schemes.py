from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime


class CategoryCreate(BaseModel):
    name: str


class CategoryReturn(BaseModel):
    id: int
    name: str


class Product(BaseModel):
    name: str
    description: str
    price: conint(ge=1)
    owner_id: int
    category_id: int


class ProductCreate(Product):
    pass


class ProductFullUpdate(Product):
    pass


class ProductPartialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[conint(ge=1)] = None
    owner_id: Optional[int] = None
    category_id: Optional[int] = None


class ProductReturn(BaseModel):
    id: int
    name: str
    description: str
    price: conint(ge=1)
    created_at: datetime
    owner_id: int
    owner: UserReturn
    category_id: int
    category: CategoryReturn