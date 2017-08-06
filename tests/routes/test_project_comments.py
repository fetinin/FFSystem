import pytest
from ffsystem.database.models import ProjectComments

project_materials_url = '/api/projects/%s/comments/'


@pytest.yield_fixture
def project_comments(project, user_lancer):
    pc = ProjectComments(
        comment='Done!',
        user_id=user_lancer.id,
        project_fk=project.id,
    )
    pc.save()
    yield pc
    pc.delete()


def test_create_project_comments(flask_app, client, user_employer, project):
    payload = {
        'comment': 'Mi first comment!',
        'userId': user_employer.id,
    }
    resp = client.post(project_materials_url % project.id, json=payload,
                       headers={'token': user_employer.token})
    assert resp.status_code == 201
    try:
        assert 'id' in resp.json
        assert resp.json['comment'] == 'Mi first comment!'
        assert resp.json['userId'] == user_employer.id
        for key in ('createdAt', 'lastUpdate', 'projectId'):
            assert key in resp.json
    finally:
        with flask_app.app_context():
            p = ProjectComments.query.filter_by(id=resp.json['id']).first()
            p.delete()


def test_list_project_comments(client, project_comments, user_lancer):
    resp = client.get(project_materials_url % project_comments.project_fk,
                      headers={'token': user_lancer.token})
    assert resp.status_code == 200
    assert resp.json[0]['id'] == project_comments.id
    assert resp.json[0]['comment'] == project_comments.comment


def test_delete_project_comment(client, project, user_admin, project_comments):
    resp = client.delete(
        project_materials_url % project.id + str(project_comments.id),
        headers={'token': user_admin.token}
    )
    assert resp.status_code == 200
    assert resp.json['message'] == 'Success.'
