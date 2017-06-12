from db.setup import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(100))
    profile_id = db.Column(db)

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_card = db.Column(db.String(25))
    raiting = db.Column(db.Float)
    avatar_link = db.Column(db.String(255))



class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class UserProjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class ProjectsMaterials(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class ProjectsComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)