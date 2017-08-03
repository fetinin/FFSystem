import itsdangerous
from ffsystem.database import db
from ffsystem.database import validators
from ffsystem.database.validators import ValidatorMixin
from itsdangerous import TimedJSONWebSignatureSerializer
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func as sql_func

from ffsystem.config import CONF
from ffsystem.database.enums import Roles, Statuses


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


class User(ValidatorMixin, DBManager, db.Model):
    __tablename__ = 'user'
    validators = {
        'username': validators.is_name,
        'password': validators.is_password,
        'role': validators.is_role,
        'credit_card': validators.is_credit_card,
        'avatar_link': validators.is_link,
    }

    id = db.Column(db.Integer, primary_key=True)
    date_registered = db.Column(db.Date, default=sql_func.now())

    username = db.Column(db.String(40), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(Roles), default=Roles.lancer.value)
    credit_card = db.Column(db.String(25), nullable=False)
    avatar_link = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'username': self.username,
            'role': self.role.value,
            'credit_card': self.credit_card,
            'avatar_link': self.avatar_link,
                }

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, password):
        self._password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expires_in=3600):
        s = TimedJSONWebSignatureSerializer(CONF['SECRET_KEY'], expires_in)
        return s.dumps({'id': self.id})

    @classmethod
    def verify_token(cls, token):
        s = itsdangerous.TimedJSONWebSignatureSerializer(CONF['SECRET_KEY'])
        try:
            data = s.loads(token)
        except itsdangerous.SignatureExpired:
            return None  # valid token, but expired
        except itsdangerous.BadSignature:
            return None  # invalid token
        return data

    @classmethod
    def get_by_auth_token(cls, token):
        user_data = cls.verify_token(token)
        if user_data:
            return cls.query.get(user_data['id'])


class Project(DBManager, ValidatorMixin, db.Model):
    __tablename__ = 'project'
    validators = {
        'name': validators.is_name,
        'description': validators.is_not_empty,
        'price': validators.are_all_digits,
        'due_to_date': validators.date_is_not_past,
        'status': validators.is_project_status,
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
        'file_link': validators.is_link,
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
        'comment': validators.is_not_empty
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
