import datetime

from ffsystem.database.enums import Statuses
from ffsystem.database.models import Project


def test_create_project(flask_app, client, user_employer, user_lancer):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    payload = {
        'name': 'test_project',
        'description': 'Do this and do that. bla bla bla',
        'price': 6500,
        'dueToDate': tomorrow.isoformat(),
        'employerId': user_employer.id,
        'lancerId': user_lancer.id,
    }
    resp = client.post('/api/projects/', json=payload,
                       headers={'token': user_employer.token})
    assert resp.status_code == 201
    try:
        assert 'id' in resp.json
        assert resp.json['dueToDate'] == str(tomorrow)
        assert resp.json['status'] == Statuses.open.value
    finally:
        with flask_app.app_context():
            Project.query.filter_by(id=resp.json['id']).first().delete()


def test_show_project(client, project, user_lancer):
    resp = client.get('/api/projects/%s' % project.id,
                      headers={'token': user_lancer.token})
    assert resp.json['id'] == project.id
    assert resp.json['name'] == project.name


def test_list_projects(client, project, user_lancer):
    resp = client.get('/api/projects/', headers={'token': user_lancer.token})
    assert len(resp.json) != 0
    assert 'id' in resp.json[0]


def test_delete_project(client, project, user_admin):
    resp = client.delete('/api/projects/%s' % project.id,
                         headers={'token': user_admin.token})
    assert resp.status_code == 200
    assert resp.json['message'] == 'Success.'


def test_edit_project(client, project, user_admin):
    resp = client.put('/api/projects/%s' % project.id,
                      json={'name': 'new_project_name'},
                      headers={'token': user_admin.token})

    assert resp.status_code == 200
    assert resp.json['name'] == 'new_project_name'
