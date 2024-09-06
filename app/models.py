from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, nullable=False)
    email = Column('email', String, nullable=False)
    username = Column('username', String, unique=True, nullable=False)
    password = Column('password', String, nullable=False)
    created_at = Column('created_at', TIMESTAMP(timezone=True), default=text('now()'))
