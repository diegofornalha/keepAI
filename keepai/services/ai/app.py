from flask import Flask
from dotenv import load_dotenv
from api.routes import ai_blueprint

# Carregar variáveis de ambiente
load_dotenv()


def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(ai_blueprint, url_prefix="/api/ai")

    @app.route("/health")
    def health_check():
        """Endpoint de verificação de saúde"""
        return {"status": "healthy", "service": "ai"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5002)
