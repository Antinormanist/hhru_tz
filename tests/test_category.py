def test_get_categories(client):
    response = client.get('/categories/')
    assert response.status_code == 200


def test_create_category(authorized_client):
    category_data = {
        'name': 'furniture'
    }
    response = authorized_client.post('/categories/', json=category_data)
    assert response.status_code == 201
    response = authorized_client.get('/categories/')
    assert response.status_code == 200
    assert response.json()[0]['name'] == category_data['name']


def test_forbidden_create_category(client):
    response = client.post('/categories/', json={'name': 'furniture'})
    assert response.status_code == 401