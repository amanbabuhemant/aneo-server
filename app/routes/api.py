from flask import Blueprint
from models.animation import Animation

api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/index")
def index():
    index = Animation.gen_index()
    return index, {'Content-Type': 'text/text'}

@api.get("/animation/<name>")
def animation_api(name):
    animation = Animation.by_name(name)
    if not animation:
        return "", 404
    return animation.content, {"Content-Type": "text/text"}

