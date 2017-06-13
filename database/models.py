import enum

from sqlalchemy.sql import func

from database import db


@enum.unique
class Roles(enum.Enum):
    admin = 'admin'
    lancer = 'lancer'
    employer = 'employer'


@enum.unique
class Statuses(enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    verification = 'verification'
    on_rework = 'on_rework'
    deploying = 'deploying'
    waiting_payment = 'waiting_payment'
    closed = 'closed'


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    registered_date = db.Column(db.Date(), default=func.now())
    login = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.Enum(Roles), nullable=False)
    credit_card = db.Column(db.String(25), nullable=False)
    rating = db.Column(db.Float(precision=2), default=0)
    avatar_link = db.Column(db.String(255), nullable=True)


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    due_to_date = db.Column(db.Date(), nullable=False)
    status = db.Column(db.Enum(Statuses), default=Statuses.open)

    lancer_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False,
    )
    employer_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False,
    )
    project_materials_id = db.Column(
        db.Integer(),
        db.ForeignKey('project_materials.id'),
        nullable=False,
    )

    # materials = db.relationship('ProjectMaterials')


class ProjectMaterials(db.Model):
    __tablename__ = 'project_materials'

    id = db.Column(db.Integer, primary_key=True)

    file_name = db.Column(db.String(100), nullable=False)
    file_link = db.Column(db.String(255), nullable=False)

    # project = db.relationship('Project', back_populates='project_materials')


class ProjectComments(db.Model):
    __tablename__ = 'project_comments'

    id = db.Column(db.Integer(), primary_key=True)

    comment = db.Column(db.Text())
    crated_at = db.Column(db.DateTime(timezone=True), default=func.now())
    last_update = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    project_id = db.Column(
        db.Integer(),
        db.ForeignKey('project.id'),
        nullable=False,
    )
    commentator_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False,
    )
