
def test_create_user_no_credentials(client):
    resp = client.post('/api/users/')
    assert resp.status_code == 400
    assert resp.json == {'error': 'Username and password are required.'}


def test_create_user_with_credentials(client):
    payload = {
        'username': 'test',
        'password': 'hey!',
        'creditCard': '4532954356226826',
    }
    resp = client.post('/api/users/', json=payload)
    assert resp.status_code == 201
    assert resp.json['username'] == 'test'
    assert 'token' in resp.json
