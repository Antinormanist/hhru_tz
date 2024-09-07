from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import get_db
from app.models import User
from app import schemes

router = APIRouter(
    tags=['Product'],
    prefix='/products'
)