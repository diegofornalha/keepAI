from server.routes.auth import auth_bp
from server.routes.tasks import tasks_bp
# Importe outros blueprints aqui

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    # Registre outros blueprints aqui
