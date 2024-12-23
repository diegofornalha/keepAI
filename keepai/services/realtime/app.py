from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from api.routes import realtime_blueprint

# Carregar variáveis de ambiente
load_dotenv()

# Configurar SocketIO
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)

    # Configurar CORS e outros middlewares
    app.config["SECRET_KEY"] = "seu-secret-key-aqui"

    # Inicializar SocketIO com a app
    socketio.init_app(app)

    # Registrar blueprints
    app.register_blueprint(realtime_blueprint, url_prefix="/api/realtime")

    # Registrar handlers de eventos
    from events import register_handlers

    register_handlers(socketio)

    @app.route("/health")
    def health_check():
        """Endpoint de verificação de saúde"""
        return {"status": "healthy", "service": "realtime"}

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5003, debug=True)
