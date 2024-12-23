"""
Módulos da aplicação Flask
Cada módulo segue a estrutura:

- controllers/: Controladores e rotas
- services/: Lógica de negócio
- schemas/: Validação e serialização
- utils/: Funções auxiliares
"""

from flask import Blueprint


# Registrar blueprints dos módulos
def register_modules(app):
    from .auth.controllers.auth_controller import auth_bp
    from .calendar.controllers.calendar_controller import calendar_bp
    from .chat.controllers.chat_controller import chat_bp
    from .notes.controllers.notes_controller import notes_bp
    from .tasks.controllers.tasks_controller import tasks_bp

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(notes_bp, url_prefix="/api/notes")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(calendar_bp, url_prefix="/api/calendar")
