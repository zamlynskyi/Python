from flask import Blueprint

friends_bp = Blueprint("friends_bp", __name__, url_prefix='/friends_bp')

from . import models
