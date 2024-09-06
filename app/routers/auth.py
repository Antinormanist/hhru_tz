from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from decouple import config

from app.database import get_db
from app.models import User
from app.utils import verify_password

router = APIRouter(
    tags=['Authentication']
)

oauth2 = OAuth2PasswordBearer(tokenUrl='/login')


def verify_token(token: str, exception):
    try:
        payload = jwt.decode(token, config('SECRET_KEY'), algorithms=[config('ALGORITHM')])
        id = payload.get('user_id')
        if id is None:
            raise exception
        return id
    except:
        raise exception


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, 'Could not validate credentials')
    id = verify_token(token, credential_exception)
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Authorized user is not found')
    return user


def create_access_token(data: dict) -> str:
    new_data = data.copy()
    new_data['exp'] = datetime.now(timezone.utc) + timedelta(minutes=config('EXPIRE_TIME_MINUTES', cast=int))
    to_encode = jwt.encode(new_data, config('SECRET_KEY'), algorithm=config('ALGORITHM'))
    return to_encode


@router.post('/login')
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if user is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid credentials')
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid credentials')
    access_token = create_access_token({'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}