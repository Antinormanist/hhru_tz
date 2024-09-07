from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config
from fastapi.testclient import TestClient
import pytest

from app.database import Base, get_db
from app.main import app
from app.routers.auth import create_access_token

DBMS = config('DBMS')
DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST_TEST')
DB_NAME = config('DB_NAME_TEST')
SQLALCHEMY_URL = f'{DBMS}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_engine(SQLALCHEMY_URL)

TestSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def create_user(client):
    user_data = {
        'email': 'email@gmail.com',
        'username': 'username',
        'password': 'password'
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    user = response.json()
    user['id'] = 1
    user['password'] = user_data['password']
    return user


@pytest.fixture
def token(create_user):
    return create_access_token({'user_id': create_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers.update({
        'Authorization': f'Bearer {token}'
    })
    return client


@pytest.fixture
def create_category(authorized_client):
    response = authorized_client.post('/categories/', json={'name': 'furniture'})
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def create_product(authorized_client, create_category):
    product_data = {
        'name': 'sofa',
        'description': 'hello world',
        'price': 120,
        'owner_id': 1,
        'category_id': create_category['id']
    }
    response = authorized_client.post('/products/', json=product_data)
    assert response.status_code == 201
    assert response.json()['name'] == product_data['name']
    return response.json()


@pytest.fixture
def create_product2(authorized_client, create_category):
    product_data = {
        'name': 'Fridge',
        'description': 'hello hell',
        'price': 500,
        'owner_id': 1,
        'category_id': create_category['id']
    }
    response = authorized_client.post('/products/', json=product_data)
    assert response.status_code == 201
    assert response.json()['name'] == product_data['name']
    return response.json()


@pytest.fixture
def create_product3(authorized_client, create_category):
    product_data = {
        'name': 'Clocks',
        'description': '12PM.',
        'price': 120,
        'owner_id': 1,
        'category_id': create_category['id']
    }
    response = authorized_client.post('/products/', json=product_data)
    assert response.status_code == 201
    assert response.json()['name'] == product_data['name']
    return response.json()