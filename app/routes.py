from flask import render_template, flash, redirect, request, session, url_for
from app import app
from app.forms import LoginForm, RegistrationForm, ForgetPassword
from flask_login import current_user, login_user, logout_user
from app.models import User, Task, Solution, Groups
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
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        # session['user_id'] = user.id
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
        return render_template('groups.html', id=id, group=group)
    groups = Groups.query.all()
    return render_template('groups.html', id=id, groups=groups)





@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')



@app.route('/contests')
def contests():
    return render_template('contests.html')



# @app.route('/create_group', methods=['GET', 'POST'])
# def create_group():
#     form = GroupForm()
#     if form.validate_on_submit():
#         new_group = Group(name=form.name.data, description=form.description.data)
#         db.session.add(new_group)
#         db.session.commit()
#         flash('Group created successfully!', 'success')
#         return redirect('/')  # Перенаправляем на главную страницу
#     return render_template('create_group.html', form=form)
#
# @app.route('/group/<int:group_id>')
# def join_group(group_id):
#     group = Group.query.get_or_404(group_id)
#     # Эмуляция текущего пользователя
#     current_user = User.query.first()  # Это пример, используйте систему аутентификации для получения реального пользователя
#     if group_id not in current_user.joined_groups:
#         current_user.joined_groups.append(group_id)
#         db.session.commit()
#         flash('You have joined the group!', 'success')
#     return redirect('groups', group_id=group.id)
#
# @app.route('/groups/<int:group_id>')
# def groups(group_id):
#     group = Groups.query.get_or_404(group_id)
#     return render_template('group.html', group=group)
#


@app.route('/join_group/<int:group_id>', methods=['POST'])
def join_group(group_id):
    # Получаем текущего пользователя (предположим, что у тебя есть система авторизации)
    current_user = User.query.filter_by(id=session['user_id']).first()
    group = Groups.query.get(group_id)

    if group and current_user:
        # Добавляем пользователя в группу
        if group not in current_user.groups:
            current_user.groups.append(group)
            db.session.commit()

    return redirect(url_for('groups'))


# @app.route('/profile')
# def profile():
#     current_user = User.query.filter_by(id=session.get('user_id')).first()
#     if current_user:
#         user_groups = current_user.groups
#         all_groups = Groups.query.all()
#         return render_template('profile.html', user_groups=user_groups, all_groups=all_groups)
#     return redirect(url_for('profile'))

@app.route('/leave_group/<int:group_id>', methods=['POST'])
def leave_group(group_id):
    # Получаем текущего пользователя
    current_user = User.query.filter_by(id=session['user_id']).first()
    group = Groups.query.get(group_id)

    if group and current_user:
        # Убираем группу из списка групп пользователя
        if group in current_user.groups:
            current_user.groups.remove(group)
            db.session.commit()

    return redirect(url_for('profile'))

@app.route('/group/<int:group_id>', methods=['GET', 'POST'])
def group_detail(group_id):
    group = Groups.query.get_or_404(group_id)
    print(current_user.id)
    user = User.query.get(current_user.id)
    print(user)
    print(user.groups)
    if request.method == 'POST':
        if group not in user.groups:
            user.groups.append(group)
            db.session.commit()
            flash('Вы успешно присоединились к группе')
        return redirect(url_for('profile'))
    return render_template('group.html', group=group, user=user)
