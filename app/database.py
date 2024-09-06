from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from decouple import config

DBMS = config('DBMS')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST')
DB_NAME = config('DB_NAME')
SQLALCHEMY_URL = f'{DBMS}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
