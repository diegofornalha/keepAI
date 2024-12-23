from typing import Any, Dict

from flask import Blueprint, jsonify, request

from ..schemas.task_schema import (
    TaskCreate,
    TaskList,
    TaskPriority,
    TaskStatus,
    TaskUpdate,
)
from ..services.task_service import TaskService

tasks_bp = Blueprint("tasks", __name__)
task_service = TaskService()


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    """Lista todas as tarefas"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    status = request.args.get("status")
    priority = request.args.get("priority", type=int)

    if status:
        tasks = task_service.get_tasks_by_status(status)
    elif priority:
        tasks = task_service.get_tasks_by_priority(priority)
    else:
        tasks = task_service.get_all_tasks()

    # Paginação básica
    start = (page - 1) * per_page
    end = start + per_page
    paginated_tasks = tasks[start:end]

    return jsonify(
        TaskList(
            tasks=paginated_tasks, total=len(tasks), page=page, per_page=per_page
        ).dict()
    )


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    """Retorna uma tarefa específica"""
    task = task_service.get_task_by_id(task_id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404


@tasks_bp.route("", methods=["POST"])
def create_task():
    """Cria uma nova tarefa"""
    data = request.get_json()
    task_data = TaskCreate(**data).dict()
    task = task_service.create_task(task_data)
    return jsonify(task), 201


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    """Atualiza uma tarefa existente"""
    data = request.get_json()
    task_data = TaskUpdate(**data).dict(exclude_unset=True)
    task = task_service.update_task(task_id, task_data)
    if task:
        return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """Remove uma tarefa"""
    task_service.delete_task(task_id)
    return "", 204


@tasks_bp.route("/search", methods=["GET"])
def search_tasks():
    """Pesquisa tarefas"""
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Parâmetro de busca não fornecido"}), 400

    tasks = task_service.search_tasks(query)
    return jsonify(tasks)


@tasks_bp.route("/overdue", methods=["GET"])
def get_overdue_tasks():
    """Lista tarefas atrasadas"""
    tasks = task_service.get_overdue_tasks()
    return jsonify(tasks)


@tasks_bp.route("/stats", methods=["GET"])
def get_task_stats():
    """Retorna estatísticas das tarefas"""
    stats = task_service.get_task_stats()
    return jsonify(stats)


@tasks_bp.route("/enums", methods=["GET"])
def get_enums():
    """Retorna enums disponíveis"""
    return jsonify(
        {
            "status": {s.name: s.value for s in TaskStatus},
            "priority": {p.name: p.value for p in TaskPriority},
        }
    )
