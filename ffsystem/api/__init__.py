from ffsystem.api.users import users_bp
from ffsystem.api.index import index_bp
from ffsystem.api.token import token_bp
from ffsystem.api.projects import projects_bp
from ffsystem.api.project_materials import pm_bp as project_materials_bp
from ffsystem.api.project_comments import pc_bp as project_comments_bp

blueprints = [
    users_bp,
    index_bp,
    token_bp,
    projects_bp,
    project_materials_bp,
    project_comments_bp,
]
