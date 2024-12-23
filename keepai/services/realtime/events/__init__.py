from flask_socketio import emit, join_room, leave_room
from typing import Dict, Any


def register_handlers(socketio):
    @socketio.on("connect")
    def handle_connect():
        """Handler para conexão de cliente"""
        emit("connected", {"status": "connected"})

    @socketio.on("disconnect")
    def handle_disconnect():
        """Handler para desconexão de cliente"""
        emit("disconnected", {"status": "disconnected"})

    @socketio.on("join")
    def handle_join(data: Dict[str, Any]):
        """Handler para entrar em uma sala"""
        room = data.get("room")
        if room:
            join_room(room)
            emit("joined", {"room": room}, room=room)

    @socketio.on("leave")
    def handle_leave(data: Dict[str, Any]):
        """Handler para sair de uma sala"""
        room = data.get("room")
        if room:
            leave_room(room)
            emit("left", {"room": room}, room=room)

    @socketio.on("message")
    def handle_message(data: Dict[str, Any]):
        """Handler para mensagens"""
        room = data.get("room")
        message = data.get("message")
        if room and message:
            emit("message", {"room": room, "message": message}, room=room)

    @socketio.on("typing")
    def handle_typing(data: Dict[str, Any]):
        """Handler para notificação de digitação"""
        room = data.get("room")
        user = data.get("user")
        if room and user:
            emit("typing", {"room": room, "user": user}, room=room)
