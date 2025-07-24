from flask import Blueprint, render_template, session, request, redirect, flash

from datetime import datetime

from models.animation import Animation

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/")
@admin.route("/dashboard")
def dashborad():
    return render_template("admin/dashboard.html")

@admin.route("/login", methods=["GET", "POST"])
def login():
    return render_template("admin/login.html")

@admin.route("/logout")
def logout():
    session.clear()
    return render_template("/")

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

