from flask import Blueprint, render_template, session, request, redirect, flash, g

from datetime import datetime

from models.animation import Animation
from models.user import User
from models.revision import Revision

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.before_request
def before_request():
    username = session.get("username", "")
    user = User.by_username(username)
    if not user and request.path != "/admin/login":
        return redirect("/admin/login")
    g.user = user


@admin.route("/")
@admin.route("/dashboard")
def dashborad():
    return render_template("admin/dashboard.html")

@admin.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = User.by_username(username)
        if user and user.match_password(password):
            session["username"] = username
            return redirect("/admin")

    return render_template("admin/login.html")

@admin.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        password = request.form.get("password", "")
        n_password = request.form.get("npassword", "")
        c_password = request.form.get("cpassword", "")
        user = g.user
        if not user.match_password(password):
            flash("Current passowrd did not match", "error")
            return redirect("/admin/change-password")
        if n_password != c_password:
            flash("New and Confirm password did not match", "error")
            return redirect("/admin/change-password")
        user.set_password(n_password)
        flash("Password updated", "success")
        
    return render_template("admin/change-password.html")

@admin.route("/logout")
def logout():
    session.clear()
    return redirect("/admin/login")

@admin.route("/new-animation", methods=["GET", "POST"])
def new_animation():
    if request.method == "POST":
        name = request.form["name"]
        title = request.form["title"]
        content = request.form["content"]
        values = { "name": name, "title": title, "content": content }
        if not Animation.valid_name(name):
            flash("Name is not valid")
            return render_template("admin/new-animation.html", **values)
        if not title:
            flash("Title is required")
            return render_template("admin/new-animation.html", **values)
        if not content:
            flash("Content is empty")
            return render_template("admin/new-animation.html", **values)
        animation = Animation.by_name(name)
        if animation:
            flash("Animation with that name already exist")
            return render_template("admin/new-animation.html", **values)
        animation = Animation.create(
            name = name,
            title = title,
        )
        animation.content = content
        if animation:
            flash("Animation created")
            return redirect("/admin/animations/" + name)

    return render_template("admin/new-animation.html")

@admin.route("/animations")
def animations():
    animations = Animation.select().order_by(Animation.id.desc())
    return render_template("admin/animations.html", animations=animations)

@admin.route("/animations/<name>")
def animation(name):
    animation = Animation.by_name(name)
    if not animation:
        flash("Animation not found with name " + name)
        return redirect("/admin/animations")
    return render_template("admin/animation.html", animation=animation)

@admin.route("/animations/<name>/edit", methods=["GET", "POST"])
def edit_animation(name):
    animation = Animation.by_name(name)
    if not animation:
        flash("Animation not found with name " + name)
        return redirect("/admin/animations")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        active = request.form["active"] == "true"
        animation.title = title
        animation.active = active
        animation.updated = datetime.utcnow()
        animation.save()
        animation.content = content
        flash("Animation updated", "success")

    return render_template("admin/edit-animation.html", animation=animation)

@admin.route("/revision")
def revesions():
    return render_template("admin/revisions.html", revisions=Revision.select().order_by(Revision.id.desc()))

@admin.route("/revision/<animation>")
def revisions_(animation):
    revisions = Revision.get_revisions_for(animation)
    return render_template("admin/revisions.html", revisions=revisions)

@admin.route("/revision/<animation>/<int:id>", methods=["GET", "POST"])
def revision_(animation, id):
    revision = Revision.get_or_none(Revision.id == id)
    if not revision:
        return redirect("/revisions/" + animation)

    if request.method == "POST":
        rollback_id = request.form.get("rollback-id", 0, int)
        if rollback_id != id:
            return redirect("/admin")
        revision.rollback()
        flash("Animation rollbacked", "success")

    return render_template("admin/revision.html", revision=revision)

