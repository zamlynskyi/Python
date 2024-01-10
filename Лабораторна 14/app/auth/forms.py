from flask import flash
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Email
from wtforms.validators import Regexp
from werkzeug.utils import secure_filename
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField("Ім'я користувача:", validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp('^[A-Za-z0-9_.]+$', message="Допускаються лише літери, цифри, крапки або підкреслення")
    ])
    email = StringField('Пошта:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердіть пароль:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Це ім'я користувача вже зайнято. Будь ласка, виберіть інше")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ця електронна пошта вже зареєстрована. Будь ласка, використовуйте іншу адресу '
                                  'електронної пошти')


class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача:", validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField('Вхід')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль:', validators=[InputRequired(), Length(min=4, max=10)])
    new_password = PasswordField('Введіть новий пароль:', validators=[InputRequired(), Length(min=4, max=10)])
    confirm_new_password = PasswordField('Введіть новий пароль ще раз:',
                                         validators=[InputRequired(), Length(min=4, max=10)])
    submit = SubmitField('Змінити')


class UpdateAccountForm(FlaskForm):
    username = StringField("Ім'я користувача:", validators=[
        DataRequired(),
        Length(min=2, max=20),
    ])
    email = StringField('Пошта:', validators=[DataRequired(), Email()])
    picture = FileField('Оновити зображення профілю', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('Про мене:', validators=[Length(max=140)])
    submit = SubmitField('Оновити')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash("Це ім'я користувача вже зайнято. Будь ласка, виберіть інше", 'danger')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                flash('Ця електронна пошта вже зареєстрована. Будь ласка, використовуйте іншу адресу електронної пошти', 'danger')
