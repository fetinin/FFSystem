from flask import jsonify, Blueprint
from werkzeug.exceptions import BadRequest, NotFound

from ffsystem.database.enums import Roles
from ffsystem.database.models import Project
from ffsystem.helpers import token_auth, role_required, extract_json

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')

allowed_project_keys = {
    'name', 'description', 'price', 'due_to_date',
    'status', 'lancer_id', 'employer_id',
}


@projects_bp.route('/', methods=['GET'])
@token_auth
def list_projects():
    projects = Project.query().all()
    projects_as_dicts = [p.to_dict() for p in projects]
    return jsonify(projects_as_dicts), 200


@projects_bp.route('/', methods=['POST'])
@token_auth
@extract_json(allowed_keys=allowed_project_keys)
def create_project(json_data):
    try:
        project = Project(**json_data)
    except ValueError as err:
        raise BadRequest(str(err))
    project.save()
    return jsonify(project.to_dict()), 201


@projects_bp.route('/<int:id>', methods=['GET'])
@token_auth
def get_project(id):
    project = Project.query(id=id).first()
    if project:
        return jsonify(project.to_dict()), 200
    else:
        raise NotFound("Project not found.")


@projects_bp.route('/<int:id>', methods=['PUT'])
@token_auth
@extract_json(allowed_keys=allowed_project_keys)
def update_project(id, json_data):
    project = Project.query(id=id).first()
    if not project:
        raise NotFound("Project not found.")
    else:
        try:
            project.update(**json_data)
        except AttributeError as err:
            raise BadRequest(str(err))
    return jsonify(project.to_dict()), 200


@projects_bp.route('/<int:id>', methods=['GET'])
@token_auth
@role_required(Roles.admin.value)
def delete_project(id):
    project = Project.query(id=id).first()
    if not project:
        raise NotFound("Project not found.")
    else:
        project.delete()
    return jsonify(message='Success.'), 200
