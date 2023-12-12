from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Email
from wtforms.validators import Regexp
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField("Ім'я користувача", validators=[
        DataRequired(),
        Length(min=2, max=20),
        Regexp('^[A-ZА-Яa-zа-я0-9_.]+$', message="Допускаються лише літери, цифри, крапки або підкреслення")
    ])
    email = StringField('Пошта', validators=[DataRequired("Недійсна адреса електронної пошти"), Email()])
    password = PasswordField('Пароль', validators=[DataRequired("Це поле є обов'язковим для заповнення")])
    confirm_password = PasswordField('Підтвердіть пароль', validators=[DataRequired("Це поле має відповідати полю паролю."), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Це ім'я користувача вже зайнято. Будь ласка, виберіть інше")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Ця електронна пошта вже зареєстрована. Будь ласка, використовуйте іншу адресу електронної пошти")


class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача", validators=[DataRequired("Це поле є обов'язковим")])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=10,
                                                                           message="Поле має бути довжиною від 4 до 10 символів")])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Вхід")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль', validators=[InputRequired("Це поле є обов'язковим"),
                                                                    Length(min=4, max=10,
                                                                           message="Це поле має бути довжиною від 4 до 10 символів")])
    new_passwords = PasswordField("Введіть новий пароль", validators=[InputRequired("Це поле є обов'язковим"),
                                                                      Length(min=4, max=10,
                                                                             message="Це поле має бути довжиною від 4 до 10 символів")])
    confirm_new_password = PasswordField("Введіть новий пароль ще раз",
                                         validators=[InputRequired("Це поле є обов'язковим"), Length(min=4, max=10,
                                                                                                     message="Це поле має бути довжиною від 4 до 10 символів")])
    submit = SubmitField("Змінити")


class TodoForm(FlaskForm):
    todo_item = StringField("Назва завдання", validators=[DataRequired()])
    description = StringField("Опис")
    status = BooleanField("Статус")
    submit = SubmitField('Зберегти')


class FeedbackForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired()])
    email = StringField("Пошта", validators=[DataRequired()])
    message = StringField("Повідомлення", validators=[DataRequired()])
    submit = SubmitField("Надіслати")
