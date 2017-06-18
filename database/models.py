from sqlalchemy.sql import func as sql_func

from database import db
from database import validators
from database.enums import Roles, Statuses
from database.validators import ValidatorMixin


class DBManager:
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        self.update(**kwargs)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(DBManager, ValidatorMixin, db.Model):
    __tablename__ = 'user'
    validators = {
        'login': validators.name,
        'password': validators.password,
        'role': validators.role,
        'credit_card': validators.credit_card,
        'avatar_link': validators.link,
    }

    id = db.Column(db.Integer, primary_key=True)
    date_registered = db.Column(db.Date, default=sql_func.now())

    login = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(Roles), nullable=False)
    credit_card = db.Column(db.String(25), nullable=False)
    avatar_link = db.Column(db.String(255))


class Project(DBManager, ValidatorMixin, db.Model):
    __tablename__ = 'project'
    validators = {
        'name': validators.name,
        'description': validators.not_empty,
        'price': validators.all_digits,
        'due_to_date': validators.date_not_past,
        'status': validators.project_status,
    }

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=sql_func.now())

    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    due_to_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(Statuses), default=Statuses.open)

    lancer_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
    employer_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )

    comments = db.relationship('ProjectComments')
    materials = db.relationship('ProjectMaterials')


class ProjectMaterials(DBManager, ValidatorMixin, db.Model):
    __tablename__ = 'project_materials'
    validators = {
        'file_link': validators.link,
    }

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=sql_func.now())

    file_name = db.Column(db.String(100), nullable=False)
    file_link = db.Column(db.String(255), nullable=False)

    project = db.relationship('Project', back_populates='materials')

    project_fk = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False,
    )


class ProjectComments(DBManager, ValidatorMixin, db.Model):
    __tablename__ = 'project_comments'
    validators = {
        'comment': validators.not_empty
    }

    id = db.Column(db.Integer, primary_key=True)
    crated_at = db.Column(db.DateTime(timezone=True), default=sql_func.now())
    last_update = db.Column(db.DateTime(timezone=True), onupdate=sql_func.now())

    comment = db.Column(db.Text, nullable=False)

    project = db.relationship('Project', back_populates='comments')

    project_fk = db.Column(
        db.Integer,
        db.ForeignKey('project.id'),
        nullable=False,
    )
    commentator_fk = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False,
    )
