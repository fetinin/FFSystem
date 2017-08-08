from flask import jsonify, Blueprint
from werkzeug.exceptions import BadRequest, NotFound

from ffsystem.database.enums import Roles
from ffsystem.database.models import ProjectMaterials
from ffsystem.helpers import token_auth, role_required, extract_json

pm_bp = Blueprint('project_materials', __name__,
                  url_prefix='/api/projects/<int:project_id>/materials')

allowed_pm_keys = {'file_name', 'file_link'}


@pm_bp.route('/', methods=['GET'])
@token_auth
def list_project_materials(project_id):
    pm = ProjectMaterials.query.filter_by(project_fk=project_id).all()
    pm_as_dicts = [p.to_dict() for p in pm]
    return jsonify(pm_as_dicts), 200


@pm_bp.route('/', methods=['POST'])
@token_auth
@extract_json(allowed_keys=allowed_pm_keys)
def create_project_material(json_data, project_id):
    try:
        pm = ProjectMaterials(**json_data, project_fk=project_id)
    except ValueError as err:
        raise BadRequest(str(err))
    pm.save()
    return jsonify(pm.to_dict()), 201


@pm_bp.route('/<int:material_id>', methods=['DELETE'])
@token_auth
@role_required(Roles.admin.value)
def delete_project_material(project_id, material_id):
    pm = ProjectMaterials.query.filter_by(id=material_id,
                                          project_fk=project_id).first()
    if not pm:
        raise NotFound("Project materials not found.")
    else:
        pm.delete()
    return jsonify(message='Success.'), 200
