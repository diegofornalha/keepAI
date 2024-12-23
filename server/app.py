from datetime import datetime
from flask import Flask
from flask_cors import CORS
from server.routes import register_routes
from server.config import Config
from server.routes.auth import get_current_user
from typing import Any, Dict


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensões
    CORS(app)

    # Registrar blueprints
    register_routes(app)

    # Adicionar contexto global para templates
    @app.context_processor
    def inject_user() -> Dict[str, Any]:
        return {"current_user": get_current_user()}

    # Adiciona o filtro datetime
    @app.template_filter("datetime")
    def format_datetime(value: Any) -> str:
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return str(value)
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y %H:%M")
        return str(value)

    return app


# Criar instância do app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
