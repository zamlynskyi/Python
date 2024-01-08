from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class TodoForm(FlaskForm):
    todo_item = StringField('Назва завдання:', validators=[DataRequired()])
    status = BooleanField('Статус')
    description = StringField('Опис:')
    submit = SubmitField('Зберегти')
