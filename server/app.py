from flask import Flask
from flask_cors import CORS
from server.routes import register_routes
from server.config import Config


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensões
    CORS(app)

    # Registrar blueprints
    register_routes(app)

    return app


# Criar instância do app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
