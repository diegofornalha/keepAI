from flask import Blueprint
from .notes import notes_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Registrar blueprints
api_v1_bp.register_blueprint(notes_bp, url_prefix="/notes")
