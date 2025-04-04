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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    groups = db.relationship('UserGroup', backref='user', lazy='dynamic')
    tasks = db.relationship('Task', backref='creator', lazy='dynamic')
    solutions = db.relationship('Solution', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_groups(self):
        return Groups.query.filter(Groups.id.in_(list(map(lambda g: g.group_id, self.groups)))).all()

    def get_tasks_status(self):
        solved_tasks = {solution.task_id: solution for solution in self.solutions}
        for i in solved_tasks:
            print(i, solved_tasks[i].points, solved_tasks[i].task.answer)

        all_tasks = Task.query.all()

        tasks_status = []
        for task in all_tasks:
            if task.id in solved_tasks:
                is_correct = str(solved_tasks[task.id].task.answer) == str(solved_tasks[task.id].points)
                status = "✅" if is_correct else "❌"
            else:
                status = "❓"

            tasks_status.append({
                'id': task.id,
                'title': task.title,
                'status': status
            })

        return tasks_status


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statement = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(60))

    answer = db.Column(db.String(60))

    solutions = db.relationship('Solution', backref='task', lazy='dynamic')

    def __repr__(self):
        return '<Task №{}>'.format(self.id)


class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    points = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Solution {}>'.format(self.task_id)


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    statement = db.Column(db.Text, nullable=True)
    admin = db.Column(db.Integer, db.ForeignKey('user.id'))

    users = db.relationship('UserGroup', backref='group', lazy='dynamic')

    def get_users(self):
        return User.query.filter(User.id in map(lambda u: u.user_id, self.users)).all()

    def __repr__(self):
        return '<Groups {}>'.format(self.title)
