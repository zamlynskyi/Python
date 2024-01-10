from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from config import config


db = SQLAlchemy()
login_manager = LoginManager()
basic_auth = HTTPBasicAuth(scheme='Bearer')


def navigation():
    return {
        'portfolio.home': 'Головна',
        'portfolio.skills': 'Скіли',
        'portfolio.resume': 'Резюме',
        'post_bp.posts': 'Пости',
        'todo.todos': 'Завдання',
        'feedback.feedbacks': 'Відгуки',
        'users.user': 'Користувачі',
        'portfolio.contacts': 'Контакти',
    }


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from .todo.views import todo
        from .feedback.views import feedback
        from .portfolio.views import portfolio
        from .auth.views import auth
        from .users.views import users
        from .api import api_bp
        from .post.views import post_bp
        app.register_blueprint(todo)
        app.register_blueprint(feedback)
        app.register_blueprint(portfolio)
        app.register_blueprint(auth)
        app.register_blueprint(users)
        app.register_blueprint(api_bp)
        app.register_blueprint(post_bp)

        return app
