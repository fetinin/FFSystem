def test_get_token_lancer(client, user_lancer):
    payload = {
        'username': user_lancer.username,
        'password': user_lancer.raw_password,
    }
    resp = client.get('/api/token/', json=payload)
    assert resp.status_code == 200
    assert 'token' in resp.json


def test_get_token_admin(client, user_admin):
    payload = {
        'username': user_admin.username,
        'password': user_admin.raw_password,
    }
    resp = client.get('/api/token/', json=payload)
    assert resp.status_code == 200
    assert 'token' in resp.json
