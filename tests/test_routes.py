import json


def test_create_user(client):
    resp = client.post('/api/users/')
    resp_json = json.loads(resp.data)
    exp_resp = {'error': 'Username and password are required.'}
    assert resp.status_code == 400
    assert resp_json == exp_resp
