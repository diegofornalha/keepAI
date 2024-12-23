from flask import Flask, render_template, jsonify, request
import os
from server.config.settings import Settings


def create_app():
    app = Flask(__name__)

    # Carregar configurações
    settings = Settings()
    app.config.from_object(settings)

    # Rotas principais
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/notes")
    def notes():
        return render_template("notes.html")

    @app.route("/calendar")
    def calendar():
        return render_template("calendar.html")

    @app.route("/tasks")
    def tasks():
        return render_template("tasks.html")

    @app.route("/api/notes", methods=["GET", "POST"])
    def handle_notes():
        if request.method == "GET":
            # Lógica para buscar notas
            return jsonify({"notes": []})
        else:
            # Lógica para criar nota
            data = request.get_json()
            return jsonify({"message": "Nota criada com sucesso"})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
