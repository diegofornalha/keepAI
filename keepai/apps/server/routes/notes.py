import logging

from flask import Blueprint, jsonify, request

from ..langchain_components.autonomous_notes import AutonomousNote
from ..langchain_components.scheduler import ActionScheduler

notes_bp = Blueprint("notes", __name__)
autonomous_note = AutonomousNote()
scheduler = ActionScheduler()


@notes_bp.route("/api/notes/create", methods=["POST"])
async def create_note():
    try:
        data = request.get_json()
        content = data.get("content")

        if not content:
            return jsonify({"error": "Conteúdo da nota é obrigatório"}), 400

        # Processa a nota e executa ações automatizadas
        try:
            result = await autonomous_note.process_note(content)

            if "error" in result:
                logging.error(f"Erro ao processar nota: {result['error']}")
                return (
                    jsonify(
                        {"error": "Erro ao processar nota. Por favor, tente novamente."}
                    ),
                    500,
                )

            # Agenda ações futuras se houver
            for action in result.get("executed_actions", []):
                if action.get("schedule"):
                    await scheduler.schedule_action(action)

            return jsonify(result)

        except Exception as e:
            logging.error(f"Erro ao processar nota: {str(e)}")
            return (
                jsonify(
                    {"error": "Erro ao processar nota. Por favor, tente novamente."}
                ),
                500,
            )

    except Exception as e:
        logging.error(f"Erro na rota de criação de nota: {str(e)}")
        return jsonify({"error": "Erro interno do servidor"}), 500
