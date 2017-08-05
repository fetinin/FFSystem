import datetime


def test_create_project(client, user_employer, user_lancer):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    payload = {
        'name': 'test_project',
        'description': 'Do this and do that. bla bla bla',
        'price': '6500',
        'dueToDate': tomorrow.isoformat(),
        'employerId': user_employer.id,
        'lancerId': user_lancer.id,
    }
    resp = client.post('/api/projects/', json=payload,
                       headers={'token': user_employer.token})
    assert resp.status_code == 201
    assert 'id' in resp.json
    assert resp.json['dueToDate'] == str(tomorrow)
