from wtforms import BooleanField, FileField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from .models import PostType


class PostForm(FlaskForm):
    title = StringField('Назва', validators=[DataRequired()])
    text = TextAreaField('Текст', validators=[DataRequired()])
    type = SelectField('Тип', choices=[(choice.name, choice.value) for choice in PostType],
                       validators=[DataRequired()])
    enabled = BooleanField('Відкрити')
    image = FileField('Зображення')
    submit = SubmitField('Зберегти')
