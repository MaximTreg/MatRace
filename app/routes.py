from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import LoginForm, RegistrationForm, ForgetPassword, AnswerForm, GroupForm, TaskGroupForm
from app.models import User, Task, Groups, UserGroup, Solution, TaskGroup
from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tasks', methods=['GET', 'POST'], defaults={'id': None})
@app.route('/tasks/<int:id>', methods=['GET', 'POST'])
def tasks(id):
    if id:
        task = Task.query.get(id)
        form = AnswerForm()
        if not current_user.is_anonymous:
            solutions = Solution.query.filter_by(user_id=current_user.id, task_id=id)
            return render_template('tasks.html', id=id, task=task, form=form, solutions=solutions)
        return render_template('tasks.html', id=id, task=task, form=form)
    tasks = Task.query.all()
    if not current_user.is_anonymous:
        tasks_status = current_user.get_tasks_status(current_user.id)
        return render_template('tasks.html', id=id, tasks=tasks, tasks_status=tasks_status)
    return render_template('tasks.html', id=id, tasks_status=tasks)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Неправильное имя или пароль')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/tasks_status')
@login_required
def tasks_status():
    tasks = current_user.get_tasks_status(current_user.id)
    return render_template('tasks_status.html', tasks=tasks)

@app.route('/submit_task/<int:task_id>', methods=['POST'])
@login_required
def submit_task(task_id):

    answer = request.form.get('answer')
    task = Task.query.get(task_id)

    is_correct = (str(task.answer) == str(answer))
    solution = Solution(task_id=task.id, user_id=current_user.id, attempt   =answer, date=datetime.now())

    db.session.add(solution)
    db.session.commit()

    flash("✅ Ответ правильный!" if is_correct else "❌ Ответ неправильный!")

    return redirect(f"/tasks/{task.id}")


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
        flash('Сообщение было отправлено на {}'.format(form.email.data))
        return redirect('/')
    return render_template('forget_password.html', form=form)


@app.route('/groups', defaults={'id': None})
@app.route('/groups/<int:id>')
def groups(id):
    if id:
        group = Groups.query.get(id)
        admin = User.query.get(group.admin)
        return render_template('group.html',  cureent_user=current_user, group=group, admin=admin, User=User, UserGroup=UserGroup, Task=Task, TaskGroup=TaskGroup)
    groups = Groups.query.all()
    return render_template('groups.html', groups=groups)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html', current_user=current_user)


@app.route('/contests')
def contests():
    return render_template('contests.html')


@app.route('/join_group/<int:group_id>', methods=['GET', 'POST'])
def join_group(group_id):
    group = Groups.query.get_or_404(group_id)
    if group not in current_user.groups.all():
        db.session.add(UserGroup(user_id=current_user.id, group_id=group.id))
        db.session.commit()
        flash('Вы успешно присоединились к группе')
    groups = Groups.query.all()
    return render_template('groups.html', groups=groups)



@app.route('/leave_group/<int:group_id>')
def leave_group(group_id):
    group = Groups.query.get(group_id)
    if group and current_user.is_authenticated:
        if group in current_user.get_groups():
            UserGroup.query.filter_by(group_id=group.id, user_id=current_user.id).delete()
            db.session.commit()
            flash("Вы покинули группу")
    groups = Groups.query.all()
    return render_template('groups.html', groups=groups)




@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if current_user.is_anonymous:
        return redirect('/')
    form = GroupForm()
    if form.validate_on_submit():
        group = Groups(title=form.title.data, statement=form.statement.data, admin=current_user.id)
        db.session.add(group)
        db.session.commit()
        flash('Вы упешно создали группу и ')
        return redirect(f'/join_group/{group.id}')
    return render_template('create_group.html', form=form)

@app.route('/add_task_group/<int:group_id>', methods=['GET', 'POST'])
def add_task_group(group_id):
    if current_user.is_anonymous:
        return redirect('/')
    form = TaskGroupForm()
    if form.validate_on_submit():
        task_id = form.id.data
        task = Task.query.get(task_id)
        group = Groups.query.get_or_404(group_id)
        if TaskGroup.query.filter_by(task_id=task_id, group_id=group_id).first() is None and task is not None:
            db.session.add(TaskGroup(task_id=task_id, group_id=group_id))
            db.session.commit()
            flash('Вы успешно добавили задачу в группу')
            return redirect(f'/groups/{group_id}')
        flash('Такая задача либо уже присутствует, либо не существует')
        return render_template('add_task_group.html', form=form)
    return render_template('add_task_group.html', form=form)