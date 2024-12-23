from flask import Blueprint, render_template
from server.routes.auth import require_auth

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/notes")
@require_auth
def notes():
    return render_template("notes.html")


@main_bp.route("/calendar")
@require_auth
def calendar():
    return render_template("calendar.html")


@main_bp.route("/tasks")
@require_auth
def tasks():
    return render_template("tasks.html")


@main_bp.route("/settings")
@require_auth
def settings():
    return render_template("settings.html")
