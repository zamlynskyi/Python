from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm


class FeedbackForm(FlaskForm):
    name = StringField("Ім'я:", validators=[DataRequired()])
    email = StringField('Пошта:', validators=[DataRequired()])
    message = StringField('Повідомлення:', validators=[DataRequired()])
    submit = SubmitField('Надіслати')
