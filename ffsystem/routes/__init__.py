from ffsystem.routes.users import users_bp
from ffsystem.routes.index import index_bp
from ffsystem.routes.token import token_bp
from ffsystem.routes.projects import projects_bp
from ffsystem.routes.project_materials import pm_bp as project_materials_bp
from ffsystem.routes.project_comments import pc_bp as project_comments_bp

blueprints = [
    users_bp,
    index_bp,
    token_bp,
    projects_bp,
    project_materials_bp,
    project_comments_bp,
]
