from flask import Flask
from flask_cors import CORS
from server.config import Config
from server.models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa extensões
    CORS(app)
    db.init_app(app)

    # Importa e registra as rotas aqui para evitar importação circular
    from server.routes import register_routes

    register_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
