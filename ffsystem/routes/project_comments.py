from flask import jsonify, Blueprint
from werkzeug.exceptions import BadRequest, NotFound

from ffsystem.database.enums import Roles
from ffsystem.database.models import ProjectComments
from ffsystem.helpers import token_auth, role_required, extract_json

pc_bp = Blueprint('project_comments', __name__,
                  url_prefix='/api/projects/<int:project_id>/comments')

allowed_pc_keys = {'comment', 'user_id'}


@pc_bp.route('/', methods=['GET'])
@token_auth
def list_project_comments(project_id):
    pc = ProjectComments.query.filter_by(project_fk=project_id).all()
    pc_as_dicts = [p.to_dict() for p in pc]
    return jsonify(pc_as_dicts), 200


@pc_bp.route('/', methods=['POST'])
@token_auth
@extract_json(allowed_keys=allowed_pc_keys)
def create_project_comment(json_data, project_id):
    try:
        pc = ProjectComments(**json_data, project_fk=project_id)
    except ValueError as err:
        raise BadRequest(str(err))
    pc.save()
    return jsonify(pc.to_dict()), 201


@pc_bp.route('/<int:comment_id>', methods=['DELETE'])
@token_auth
@role_required(Roles.admin.value)
def delete_project_comment(project_id, comment_id):
    pc = ProjectComments.query.filter_by(id=comment_id,
                                         project_fk=project_id).first()
    if not pc:
        raise NotFound("Project comment not found.")
    else:
        pc.delete()
    return jsonify(message='Success.'), 200
