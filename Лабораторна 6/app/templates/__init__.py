import flask
from . import views

app = flask.Flask(__name__)
app.secret_key = b"secret"
