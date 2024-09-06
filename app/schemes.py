from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    username: str


class UserCreate(User):
    password: str


class UserUpdate(User):
    password: str


class UserPartialUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserReturn(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime