from flask import Blueprint
from .admin import admin
from .api import api


routes = Blueprint("routes", "routes")

routes.register_blueprint(admin)
routes.register_blueprint(api)
