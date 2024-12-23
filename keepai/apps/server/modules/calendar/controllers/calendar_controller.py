from flask import Blueprint, jsonify, request

from ..schemas.calendar_schema import EventSchema
from ..services.calendar_service import CalendarService

calendar_bp = Blueprint("calendar", __name__)
calendar_service = CalendarService()


@calendar_bp.route("/events", methods=["GET"])
def get_events():
    """Retorna todos os eventos do calendário"""
    events = calendar_service.get_all_events()
    return jsonify(events)


@calendar_bp.route("/events", methods=["POST"])
def create_event():
    """Cria um novo evento"""
    data = request.get_json()
    event = calendar_service.create_event(data)
    return jsonify(event), 201


@calendar_bp.route("/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    """Atualiza um evento existente"""
    data = request.get_json()
    event = calendar_service.update_event(event_id, data)
    return jsonify(event)


@calendar_bp.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """Remove um evento"""
    calendar_service.delete_event(event_id)
    return "", 204
