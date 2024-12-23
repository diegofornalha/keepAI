from server.app import db
from flask_login import UserMixin
from datetime import datetime
import json


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(200))
    _preferences = db.Column("preferences", db.Text, default="{}")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relacionamentos
    notes = db.relationship("Note", backref="user", lazy=True)
    tasks = db.relationship("Task", backref="user", lazy=True)
    events = db.relationship("Event", backref="user", lazy=True)

    @property
    def preferences(self):
        return json.loads(self._preferences)

    @preferences.setter
    def preferences(self, value):
        self._preferences = json.dumps(value)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "avatar": self.avatar,
            "preferences": self.preferences,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.email}>"
