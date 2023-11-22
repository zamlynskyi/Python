from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired


class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача:", validators=[DataRequired("Це поле є обов'язковим")])
    password = PasswordField("Пароль:", validators=[DataRequired(), Length(min=4, max=10, message="Поле має бути довжиною від 4 до 10 символів")])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Вхід")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль', validators=[InputRequired("Це поле є обов'язковим"), Length(min=4, max=10, message="Це поле має бути довжиною від 4 до 10 символів")])
    new_passwords = PasswordField("Введіть новий пароль", validators=[InputRequired("Це поле є обов'язковим"), Length(min=4, max=10, message="Це поле має бути довжиною від 4 до 10 символів")])
    confirm_new_password = PasswordField("Введіть новий пароль ще раз", validators=[InputRequired("Це поле є обов'язковим"), Length(min=4, max=10, message="Це поле має бути довжиною від 4 до 10 символів")])
    submit = SubmitField("Змінити")

