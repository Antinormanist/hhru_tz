from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, nullable=False)
    email = Column('email', String, nullable=False)
    username = Column('username', String, unique=True, nullable=False)
    password = Column('password', String, nullable=False)
    created_at = Column('created_at', TIMESTAMP(timezone=True), default=text('now()'))


class Category(Base):
    __tablename__ = 'categories'
    id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', String, unique=True, nullable=False)


class Product(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column('name', String, nullable=False)
    description = Column('description', String)
    price = Column('price', Integer, nullable=False)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship(User)
    category_id = Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    category = relationship(Category)
    created_at = Column('created_at', TIMESTAMP(timezone=True), default=text('now()'), nullable=False)