from flask import Blueprint
from .admin import admin


routes = Blueprint("routes", "routes")

routes.register_blueprint(admin)
