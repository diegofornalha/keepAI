from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from server.models.note import Note
from server.models.task import Task
from server.models.event import Event
from server.app import db
from datetime import datetime

api_bp = Blueprint("api", __name__)


# Rotas para Notas
@api_bp.route("/notes", methods=["GET"])
@login_required
def get_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return jsonify([note.to_dict() for note in notes])


@api_bp.route("/notes", methods=["POST"])
@login_required
def create_note():
    data = request.get_json()
    note = Note(title=data["title"], content=data["content"], user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201


@api_bp.route("/notes/<int:note_id>", methods=["PUT"])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.get_json()
    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)
    note.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(note.to_dict())


@api_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({"error": "Não autorizado"}), 403

    db.session.delete(note)
    db.session.commit()
    return "", 204


# Rotas para Tarefas
@api_bp.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks])


@api_bp.route("/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()
    task = Task(
        title=data["title"],
        description=data.get("description"),
        due_date=(
            datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        ),
        priority=data.get("priority", "medium"),
        list_id=data.get("list_id"),
        user_id=current_user.id,
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.due_date = (
        datetime.fromisoformat(data["due_date"])
        if data.get("due_date")
        else task.due_date
    )
    task.priority = data.get("priority", task.priority)
    task.completed = data.get("completed", task.completed)
    task.list_id = data.get("list_id", task.list_id)
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(task.to_dict())


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Não autorizado"}), 403

    db.session.delete(task)
    db.session.commit()
    return "", 204


# Rotas para Eventos
@api_bp.route("/events", methods=["GET"])
@login_required
def get_events():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return jsonify([event.to_dict() for event in events])


@api_bp.route("/events", methods=["POST"])
@login_required
def create_event():
    data = request.get_json()
    event = Event(
        title=data["title"],
        description=data.get("description"),
        start_time=datetime.fromisoformat(data["start"]),
        end_time=datetime.fromisoformat(data["end"]),
        color=data.get("color", "#2563eb"),
        user_id=current_user.id,
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 201


@api_bp.route("/events/<int:event_id>", methods=["PUT"])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        return jsonify({"error": "Não autorizado"}), 403

    data = request.get_json()
    event.title = data.get("title", event.title)
    event.description = data.get("description", event.description)
    event.start_time = (
        datetime.fromisoformat(data["start"]) if data.get("start") else event.start_time
    )
    event.end_time = (
        datetime.fromisoformat(data["end"]) if data.get("end") else event.end_time
    )
    event.color = data.get("color", event.color)
    event.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(event.to_dict())


@api_bp.route("/events/<int:event_id>", methods=["DELETE"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        return jsonify({"error": "Não autorizado"}), 403

    db.session.delete(event)
    db.session.commit()
    return "", 204


# Rotas para Usuário
@api_bp.route("/user/profile", methods=["GET"])
@login_required
def get_profile():
    return jsonify(current_user.to_dict())


@api_bp.route("/user/profile", methods=["PUT"])
@login_required
def update_profile():
    data = request.get_json()
    current_user.name = data.get("name", current_user.name)
    current_user.email = data.get("email", current_user.email)
    current_user.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(current_user.to_dict())


@api_bp.route("/user/preferences", methods=["GET"])
@login_required
def get_preferences():
    return jsonify(current_user.preferences)


@api_bp.route("/user/preferences", methods=["PUT"])
@login_required
def update_preferences():
    data = request.get_json()
    current_user.preferences.update(data)
    db.session.commit()
    return jsonify(current_user.preferences)
