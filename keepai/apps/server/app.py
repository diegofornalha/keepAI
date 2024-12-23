from typing import Optional

from flask import Flask, g, render_template
from flask_cors import CORS

from keepai.apps.server.config.security import SecurityConfig
from keepai.apps.server.config.settings import Settings
from keepai.apps.server.core.container import Container
from keepai.apps.server.modules import register_modules
from keepai.apps.server.utils.logger import setup_logger


def create_app(config_object: Optional[Settings] = None) -> Flask:
    """Application Factory Pattern do Flask

    Args:
        config_object: Objeto de configuração opcional

    Returns:
        Flask: Aplicação Flask configurada
    """
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
    security.configure(app)

    # Criar container de dependências
    container = Container(app)
    app.container = container

    # Registrar módulos
    register_modules(app)

    # Registrar rotas base
    register_base_routes(app)

    @app.before_request
    def before_request():
        """Disponibiliza o container para os módulos"""
        g.container = app.container

    return app


def register_base_routes(app: Flask) -> None:
    """Registra as rotas base da aplicação

    Args:
        app: Aplicação Flask
    """

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "environment": app.config.get("ENV", "production"),
            "debug": app.config.get("DEBUG", False),
        }


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=app.config.get("DEBUG", False))
