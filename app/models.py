from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # # groups = db.Column(db.Integer, db.ForeignKey('groups.id'))
    # group = db.relationship('User_group', backref="id_user", lazy='dynamic')
    # joined_groups = db.Column(db.PickleType, default=[])
    # solutions = db.relationship('Solution', backref='user', lazy='dynamic')
    # tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statement = db.Column(db.String)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(60))
    generate = db.Column()
    solutions = db.relationship('Solution', backref='task', lazy='dynamic')

    def __repr__(self):
        return '<Task №{}>'.format(self.id)


class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_task = db.Column(db.Integer, db.ForeignKey('task.id'))
    points = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Solution {}>'.format(self.number_of_task)


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # user = db.relationship('User', backref='id_group', lazy='dynamic')

    def __repr__(self):
        return '<Groups {}{}{}>'.format(self.title, self.id, self.statement)


# class UserGroup(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     joined_at = db.Column(db.DateTime, default=db.func.now())
#
#     user = db.relationship('User', backref='user_groups')
#     group = db.relationship('Group', backref='user_groups')


# class User_group(db.Model):
#     id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
#     id_group = db.Column(db.Integer, db.ForeignKey('groups.id'))
#     type = db.Column(db.Integer)
#
#     def __repr__(self):
#         return '<User_group {}>'.format(self.type)