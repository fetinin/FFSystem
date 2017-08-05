def test_create_user_no_credentials(client):
    resp = client.post('/api/users/', json={'year': 1518})
    assert resp.status_code == 400
    assert resp.json['message'] == 'The following items are not allowed: year'


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


def test_create_user_with__invalid_credentials(client):
    payload = {
        'username': 'test123123',
        'password': 'hey!',
        'creditCard': 'not_credit_card',
    }
    resp = client.post('/api/users/', json=payload)
    assert resp.status_code == 400
    assert resp.json['message'] == 'Credit card number should be at least 16' \
                                   ' digits long and be valid.'

