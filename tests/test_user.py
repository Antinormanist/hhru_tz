def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 200


def test_get_users_existed(client, create_user):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json()[0]['username'] == create_user['username']