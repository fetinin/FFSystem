import pytest
from ffsystem.database.models import ProjectMaterials

project_materials_url = '/api/projects/%s/materials/'


@pytest.yield_fixture
def project_materials(project):
    pm = ProjectMaterials(
        file_name='My pretty website',
        file_link='/link-to-file/site.zip',
        project_fk=project.id,
    )
    pm.save()
    yield pm
    pm.delete()


def test_create_project_materials(flask_app, client, user_employer, project):
    payload = {
        'fileName': 'My pretty website',
        'fileLink': '/link-to-file/site.zip',
    }
    resp = client.post(project_materials_url % project.id, json=payload,
                       headers={'token': user_employer.token})
    assert resp.status_code == 201
    try:
        assert 'id' in resp.json
        assert resp.json['fileName'] == 'My pretty website'
        assert resp.json['fileLink'] == '/link-to-file/site.zip'
    finally:
        with flask_app.app_context():
            p = ProjectMaterials.query.filter_by(id=resp.json['id']).first()
            p.delete()


def test_list_project_materials(client, project_materials, user_lancer):
    resp = client.get(project_materials_url % project_materials.project_fk,
                      headers={'token': user_lancer.token})
    assert resp.json[0]['id'] == project_materials.id
    assert resp.json[0]['fileName'] == project_materials.file_name


def test_delete_project_material(client, project, user_admin,
                                 project_materials):
    resp = client.delete(
        project_materials_url % project.id + str(project_materials.id),
        headers={'token': user_admin.token}
    )
    assert resp.status_code == 200
    assert resp.json['message'] == 'Success.'
