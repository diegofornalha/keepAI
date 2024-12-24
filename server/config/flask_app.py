"""Configuração principal do aplicativo Flask."""

from flask import Flask
from server.config.database import init_db
from server.routes import register_routes
from server.utils.config import load_config


def create_app() -> Flask:
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    # Carrega configurações
    config = load_config()
    app.config.update(config)

    # Inicializa banco de dados
    init_db(app)

    # Registra rotas
    register_routes(app)

    return app


# Criar instância do app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
