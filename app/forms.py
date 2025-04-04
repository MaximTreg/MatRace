from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class RegistrationForm(FlaskForm):
    email = EmailField('Ваша электронная почта', validators=[DataRequired(message=''), Email()])
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', 'Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с этим именем уже зарегистрирован')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с этой почтой уже зарегистрирован')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class ForgetPassword(FlaskForm):
    email = EmailField('Ваша электронная почта', validators=[DataRequired()])
    submit = SubmitField('Востановить')

class AnswerForm(FlaskForm):
    answer = StringField('Ответ:', validators=[DataRequired()])
    submit = SubmitField('Проверить')


class GroupForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    statement = StringField('Описание', validators=[DataRequired()])
    submit = SubmitField('Создать группу')

