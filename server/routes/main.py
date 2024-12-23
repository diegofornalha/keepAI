from flask import Blueprint, render_template
from flask_login import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    return render_template("index.html")


@main_bp.route("/notes")
@login_required
def notes():
    return render_template("notes.html")


@main_bp.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")


@main_bp.route("/tasks")
@login_required
def tasks():
    return render_template("tasks.html")


@main_bp.route("/settings")
@login_required
def settings():
    return render_template("settings.html")
