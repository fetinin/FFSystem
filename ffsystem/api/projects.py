from flask import jsonify, Blueprint
from werkzeug.exceptions import BadRequest, NotFound

from ffsystem.database.enums import Roles
from ffsystem.database.models import Project
from ffsystem.helpers import token_auth, role_required, extract_json, \
    format_dict_diff
from ffsystem.bots.telegram_bot import telebot_ffs_group as ffs_bot

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')

allowed_project_keys = {
    'name', 'description', 'price', 'due_to_date',
    'status', 'lancer_id', 'employer_id',
}


@projects_bp.route('/', methods=['GET'])
@token_auth
def list_projects():
    projects = Project.query.all()
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
    ffs_bot.send_msg(f"Появился заказ '{project.name}'!")
    return jsonify(project.to_dict()), 201


@projects_bp.route('/<int:id>', methods=['GET'])
@token_auth
def get_project(id):
    project = Project.query.filter_by(id=id).first()
    if project:
        return jsonify(project.to_dict()), 200
    else:
        raise NotFound("Project not found.")


@projects_bp.route('/<int:id>', methods=['PUT'])
@token_auth
@extract_json(allowed_keys=allowed_project_keys)
def update_project(json_data, id):
    project = Project.query.filter_by(id=id).first()
    old_project_info = project.to_dict()
    if not project:
        raise NotFound("Project not found.")
    else:
        try:
            project.update(**json_data)
        except AttributeError as err:
            raise BadRequest(str(err))
    updated_info = "\n\t".join(format_dict_diff(old_project_info, json_data))
    ffs_bot.send_msg(f"Заказ {project.name} обновился. Новая инфа: "
                     f"<pre>{updated_info}.</pre>", parse_mode='html')
    return jsonify(project.to_dict()), 200


@projects_bp.route('/<int:id>', methods=['DELETE'])
@token_auth
@role_required(Roles.admin.value)
def delete_project(id):
    project = Project.query.filter_by(id=id).first()
    if not project:
        raise NotFound("Project not found.")
    else:
        project.delete()
    return jsonify(message='Success.'), 200
