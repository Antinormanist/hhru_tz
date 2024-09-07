def test_get_products(client):
    response = client.get('/products/')
    assert response.status_code == 200


def test_get_filtered_by_create_asc_products(client, create_product, create_product2, create_product3, create_user):
    response = client.get('/products?create_asc=True')
    a, b, c = response.json()
    assert a == create_product and b == create_product2 and c == create_product3
    assert a['owner_id'] == create_user['id']


def test_get_filtered_by_create_desc_products(client, create_product, create_product2, create_product3):
    response = client.get('/products?create_desc=True')
    a, b, c = response.json()
    assert a == create_product3 and b == create_product2 and c == create_product


def test_get_filtered_by_price_asc_products(client, create_product, create_product2, create_product3):
    response = client.get('/products?price_asc=True')
    a, b, c = response.json()
    assert c == create_product2


def test_get_filtered_by_price_desc_products(client, create_product, create_product2, create_product3):
    response = client.get('/products?price_desc=True')
    a, b, c = response.json()
    assert a == create_product2


def test_get_filtered_by_search_products(client, create_product, create_product2, create_product3):
    response = client.get('/products?search=fri')
    assert response.json()[0] == create_product2


def test_update_product(authorized_client, create_product):
    category = authorized_client.post('/categories/', json={'name': 'fridge'})
    product_data = {
        'name': 'New product',
        'description': 'g',
        'price': 999,
        'owner_id': 1,
        'category_id': category.json()['id']
    }
    response = authorized_client.put(f'/products/{create_product['id']}/', json=product_data)
    assert response.status_code == 200
    assert response.json()['category_id'] == category.json()['id']
    assert response.json()['name'] == product_data['name']


def test_invalid_update_product(authorized_client):
    category = authorized_client.post('/categories/', json={'name': 'fridge'})
    product_data = {
        'name': 'New product',
        'description': 'g',
        'price': 999,
        'owner_id': 1,
        'category_id': category.json()['id']
    }
    response = authorized_client.put(f'/products/1/', json=product_data)
    assert response.status_code == 404


def test_partial_update_product(authorized_client, create_product):
    product_data = {
        'name': 'New product'
    }
    response = authorized_client.patch(f'/products/{create_product['id']}/', json=product_data)
    assert response.status_code == 200
    assert response.json()['name'] == product_data['name']
    assert response.json()['price'] == create_product['price']


def test_invalid_partial_update_product(authorized_client):
    product_data = {
        'name': 'New product'
    }
    response = authorized_client.patch(f'/products/1/', json=product_data)
    assert response.status_code == 404


def test_delete_product(authorized_client, create_product):
    response = authorized_client.delete(f'/products/{create_product['id']}')
    assert response.status_code == 204


def test_delete_invalid_product(authorized_client):
    response = authorized_client.delete(f'/products/1')
    assert response.status_code == 404