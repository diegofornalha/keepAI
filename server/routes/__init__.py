from flask import Flask
from server.routes.main import main_bp
from server.routes.auth import auth_bp
from server.routes.api.v1 import api_v1_bp


def register_routes(app: Flask) -> None:
    # Registra o blueprint principal
    app.register_blueprint(main_bp)

    # Registra os outros blueprints com seus prefixos
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")
