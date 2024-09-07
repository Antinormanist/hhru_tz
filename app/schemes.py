from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


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