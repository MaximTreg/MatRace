from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    group = db.Column(db.Integer, db.ForeignKey('groups.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    groups = db.relationship('UserGroup', backref='user', lazy='dynamic')


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
    date = db.Column(db.DateTime, index=True, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Solution {}>'.format(self.number_of_task)


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    statement = db.Column(db.Text, nullable=True)

    users = db.relationship('UserGroup', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Groups {}>'.format(self.title)
