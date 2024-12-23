from flask import Flask
from flask_cors import CORS
from server.config.settings import Settings
from server.modules.ai.controllers.agent_controller import ai_bp
from server.modules.auth.controllers.auth_controller import auth_bp
from server.modules.calendar.controllers.calendar_controller import calendar_bp
from server.modules.chat.controllers.chat_controller import chat_bp
from server.modules.notes.controllers.notes_controller import notes_bp
from server.modules.tasks.controllers.tasks_controller import tasks_bp


def create_app():
    """Cria e configura a aplicação Flask"""

    # Carregar configurações
    settings = Settings()

    # Criar aplicação
    app = Flask(__name__)

    # Configurar CORS
    CORS(app)

    # Configurar a aplicação
    app.config.from_object(settings)

    # Registrar blueprints
    app.register_blueprint(calendar_bp, url_prefix="/api/calendar")
    app.register_blueprint(notes_bp, url_prefix="/api/notes")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")

    # Rota de status
    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "supabase": bool(settings.SUPABASE_URL and settings.SUPABASE_KEY),
        }

    return app
