"""Arquivo WSGI para servir a aplicação em produção."""

from server.config.flask_app import app

if __name__ == "__main__":
    app.run()
