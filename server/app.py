from flask import Flask, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from clerk_sdk.flask import ClerkFlask

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Flask
app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates",
)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-123")

# Configuração do Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Configuração do Clerk
clerk = ClerkFlask(app)

# Inicializar extensões
CORS(app)

# Importar blueprints
from server.routes.auth import auth_bp  # noqa: E402
from server.routes.main import main_bp  # noqa: E402
from server.routes.api import api_bp  # noqa: E402

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp, url_prefix="/api")


# Rota principal
@app.route("/")
def index():
    return render_template("index.html")


# Health check
@app.route("/health")
def health():
    try:
        # Verificar conexão com o Supabase
        supabase.table("users").select("*").limit(1).execute()
        db_status = True
    except Exception:
        db_status = False

    status = "healthy" if db_status else "unhealthy"
    code = 200 if status == "healthy" else 500

    return {
        "status": status,
        "database": "connected" if db_status else "disconnected",
    }, code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
