from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, RegistrationForm, ForgetPassword
from flask_login import current_user, login_user, logout_user
from app.models import User, Task, Solution
from app import db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks', defaults={'id': None})
@app.route('/tasks/<int:id>')
def tasks(id):
    if id:
        task = Task.query.get(id)
        return render_template('tasks.html', id=id, task=task)
    tasks = Task.query.all()
    return render_template('tasks.html', id=id, tasks=tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        flash('Поздравляем, теперь вы зарегистрированный пользователь!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPassword()
    if form.validate_on_submit():
        flash('Password sent by email {}'.format(form.email.data))
        return redirect('/')
    return render_template('forget_password.html', form=form)




@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/contests')
def contests():
    return render_template('contests.html')


@app.route('/groups')
def groups():
    return render_template('groups.html')
