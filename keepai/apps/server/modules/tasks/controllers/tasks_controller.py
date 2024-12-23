from typing import Any, Dict

from flask import Blueprint, jsonify, request
from flasgger import swag_from

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
    """
    Lista todas as tarefas
    ---
    tags:
      - Tarefas
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Número da página
      - name: per_page
        in: query
        type: integer
        default: 10
        description: Itens por página
      - name: status
        in: query
        type: string
        enum: [pending, in_progress, completed, cancelled]
        description: Filtrar por status
      - name: priority
        in: query
        type: integer
        enum: [1, 2, 3, 4]
        description: Filtrar por prioridade (1=baixa, 2=média, 3=alta, 4=urgente)
    responses:
      200:
        description: Lista de tarefas
        schema:
          type: object
          properties:
            tasks:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  description:
                    type: string
                  due_date:
                    type: string
                    format: date-time
                  priority:
                    type: integer
                    enum: [1, 2, 3, 4]
                  status:
                    type: string
                    enum: [pending, in_progress, completed, cancelled]
                  tags:
                    type: array
                    items:
                      type: string
            total:
              type: integer
            page:
              type: integer
            per_page:
              type: integer
    """
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
    """
    Retorna uma tarefa específica
    ---
    tags:
      - Tarefas
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID da tarefa
    responses:
      200:
        description: Tarefa encontrada
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            due_date:
              type: string
              format: date-time
            priority:
              type: integer
              enum: [1, 2, 3, 4]
            status:
              type: string
              enum: [pending, in_progress, completed, cancelled]
            tags:
              type: array
              items:
                type: string
      404:
        description: Tarefa não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    task = task_service.get_task_by_id(task_id)
    if task:
        return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404


@tasks_bp.route("", methods=["POST"])
def create_task():
    """
    Cria uma nova tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              description: Título da tarefa
            description:
              type: string
              description: Descrição da tarefa
            due_date:
              type: string
              format: date-time
              description: Data de vencimento
            priority:
              type: integer
              enum: [1, 2, 3, 4]
              description: Prioridade (1=baixa, 2=média, 3=alta, 4=urgente)
            status:
              type: string
              enum: [pending, in_progress, completed, cancelled]
              description: Status da tarefa
            tags:
              type: array
              items:
                type: string
              description: Tags da tarefa
    responses:
      201:
        description: Tarefa criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            due_date:
              type: string
              format: date-time
            priority:
              type: integer
            status:
              type: string
            tags:
              type: array
              items:
                type: string
    """
    data = request.get_json()
    task_data = TaskCreate(**data).dict()
    task = task_service.create_task(task_data)
    return jsonify(task), 201


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    """
    Atualiza uma tarefa existente
    ---
    tags:
      - Tarefas
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID da tarefa
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Título da tarefa
            description:
              type: string
              description: Descrição da tarefa
            due_date:
              type: string
              format: date-time
              description: Data de vencimento
            priority:
              type: integer
              enum: [1, 2, 3, 4]
              description: Prioridade (1=baixa, 2=média, 3=alta, 4=urgente)
            status:
              type: string
              enum: [pending, in_progress, completed, cancelled]
              description: Status da tarefa
            tags:
              type: array
              items:
                type: string
              description: Tags da tarefa
    responses:
      200:
        description: Tarefa atualizada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            due_date:
              type: string
              format: date-time
            priority:
              type: integer
            status:
              type: string
            tags:
              type: array
              items:
                type: string
      404:
        description: Tarefa não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    task_data = TaskUpdate(**data).dict(exclude_unset=True)
    task = task_service.update_task(task_id, task_data)
    if task:
        return jsonify(task)
    return jsonify({"error": "Tarefa não encontrada"}), 404


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """
    Remove uma tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: ID da tarefa
    responses:
      204:
        description: Tarefa removida com sucesso
      404:
        description: Tarefa não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    task_service.delete_task(task_id)
    return "", 204


@tasks_bp.route("/search", methods=["GET"])
def search_tasks():
    """
    Pesquisa tarefas
    ---
    tags:
      - Tarefas
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Termo de busca
    responses:
      200:
        description: Resultados da pesquisa
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              due_date:
                type: string
                format: date-time
              priority:
                type: integer
              status:
                type: string
              tags:
                type: array
                items:
                  type: string
      400:
        description: Parâmetro de busca não fornecido
        schema:
          type: object
          properties:
            error:
              type: string
    """
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Parâmetro de busca não fornecido"}), 400

    tasks = task_service.search_tasks(query)
    return jsonify(tasks)


@tasks_bp.route("/overdue", methods=["GET"])
def get_overdue_tasks():
    """
    Lista tarefas atrasadas
    ---
    tags:
      - Tarefas
    responses:
      200:
        description: Lista de tarefas atrasadas
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              description:
                type: string
              due_date:
                type: string
                format: date-time
              priority:
                type: integer
              status:
                type: string
              tags:
                type: array
                items:
                  type: string
    """
    tasks = task_service.get_overdue_tasks()
    return jsonify(tasks)


@tasks_bp.route("/stats", methods=["GET"])
def get_task_stats():
    """
    Retorna estatísticas das tarefas
    ---
    tags:
      - Tarefas
    responses:
      200:
        description: Estatísticas das tarefas
        schema:
          type: object
          properties:
            total:
              type: integer
              description: Total de tarefas
            pending:
              type: integer
              description: Tarefas pendentes
            in_progress:
              type: integer
              description: Tarefas em andamento
            completed:
              type: integer
              description: Tarefas concluídas
            cancelled:
              type: integer
              description: Tarefas canceladas
            overdue:
              type: integer
              description: Tarefas atrasadas
    """
    stats = task_service.get_task_stats()
    return jsonify(stats)


@tasks_bp.route("/enums", methods=["GET"])
def get_enums():
    """
    Retorna enums disponíveis
    ---
    tags:
      - Tarefas
    responses:
      200:
        description: Enums disponíveis
        schema:
          type: object
          properties:
            status:
              type: object
              additionalProperties:
                type: string
              description: Status possíveis para tarefas
            priority:
              type: object
              additionalProperties:
                type: integer
              description: Níveis de prioridade disponíveis
    """
    return jsonify(
        {
            "status": {s.name: s.value for s in TaskStatus},
            "priority": {p.name: p.value for p in TaskPriority},
        }
    )
