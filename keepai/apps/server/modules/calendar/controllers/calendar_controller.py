from flask import Blueprint, jsonify, request
from flasgger import swag_from

from ..schemas.calendar_schema import EventSchema
from ..services.calendar_service import CalendarService

calendar_bp = Blueprint("calendar", __name__)
calendar_service = CalendarService()


@calendar_bp.route("/events", methods=["GET"])
def get_events():
    """
    Retorna todos os eventos do calendário
    ---
    tags:
      - Calendário
    responses:
      200:
        description: Lista de eventos
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
              start_date:
                type: string
                format: date-time
              end_date:
                type: string
                format: date-time
              all_day:
                type: boolean
              recurrence:
                type: object
                description: Configurações de recorrência do evento
    """
    events = calendar_service.get_all_events()
    return jsonify(events)


@calendar_bp.route("/events", methods=["POST"])
def create_event():
    """
    Cria um novo evento
    ---
    tags:
      - Calendário
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - start_date
            - end_date
          properties:
            title:
              type: string
              description: Título do evento
            description:
              type: string
              description: Descrição do evento
            start_date:
              type: string
              format: date-time
              description: Data e hora de início
            end_date:
              type: string
              format: date-time
              description: Data e hora de término
            all_day:
              type: boolean
              description: Se é um evento que dura o dia todo
            recurrence:
              type: object
              description: Configurações de recorrência do evento
    responses:
      201:
        description: Evento criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            start_date:
              type: string
              format: date-time
            end_date:
              type: string
              format: date-time
            all_day:
              type: boolean
            recurrence:
              type: object
    """
    data = request.get_json()
    event = calendar_service.create_event(data)
    return jsonify(event), 201


@calendar_bp.route("/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    """
    Atualiza um evento existente
    ---
    tags:
      - Calendário
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: ID do evento
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Título do evento
            description:
              type: string
              description: Descrição do evento
            start_date:
              type: string
              format: date-time
              description: Data e hora de início
            end_date:
              type: string
              format: date-time
              description: Data e hora de término
            all_day:
              type: boolean
              description: Se é um evento que dura o dia todo
            recurrence:
              type: object
              description: Configurações de recorrência do evento
    responses:
      200:
        description: Evento atualizado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            description:
              type: string
            start_date:
              type: string
              format: date-time
            end_date:
              type: string
              format: date-time
            all_day:
              type: boolean
            recurrence:
              type: object
      404:
        description: Evento não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    event = calendar_service.update_event(event_id, data)
    return jsonify(event)


@calendar_bp.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """
    Remove um evento
    ---
    tags:
      - Calendário
    parameters:
      - name: event_id
        in: path
        type: integer
        required: true
        description: ID do evento
    responses:
      204:
        description: Evento removido com sucesso
      404:
        description: Evento não encontrado
        schema:
          type: object
          properties:
            error:
              type: string
    """
    calendar_service.delete_event(event_id)
    return "", 204
