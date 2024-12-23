import os
import sys

# Adicionar o diretório atual ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from flask import Flask, render_template
from flask_cors import CORS

from config.security import SecurityConfig
from config.settings import Settings
from modules import register_modules
from utils.logger import setup_logger


def create_app(config_object=None):
    """Application Factory Pattern do Flask"""
    app = Flask(__name__)

    # Configurar logger
    setup_logger()

    # Carregar configurações
    settings = config_object or Settings()
    app.config.from_object(settings)

    # Configurar CORS
    CORS(app)

    # Configurar segurança
    security = SecurityConfig()
    for header, value in security.SECURE_HEADERS.items():
        app.config[f"SECURITY_{header}"] = value

    # Registrar módulos
    register_modules(app)

    # Rota principal
    @app.route("/")
    def index():
        return render_template("index.html")

    # Rota de healthcheck
    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "environment": app.config.get("ENV", "production"),
            "debug": app.config.get("DEBUG", False),
        }

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=app.config.get("DEBUG", False))
