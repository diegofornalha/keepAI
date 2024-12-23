import os
from typing import Any, Dict

import requests


class AuthService:
    def __init__(self):
        self.api_key = os.getenv("CLERK_SECRET_KEY")
        self.base_url = "https://api.clerk.dev/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/sessions/{token}", headers=self.headers
            )
            response.raise_for_status()
            session = response.json()
            return {
                "success": True,
                "user_id": session["user_id"],
                "session_id": session["id"],
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user(self, user_id: str) -> Dict[str, Any]:
        try:
            response = requests.get(
                f"{self.base_url}/users/{user_id}", headers=self.headers
            )
            response.raise_for_status()
            user = response.json()
            return {
                "success": True,
                "user": {
                    "id": user["id"],
                    "email": user["email_addresses"][0]["email_address"],
                    "first_name": user.get("first_name", ""),
                    "last_name": user.get("last_name", ""),
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def handle_webhook(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if event_type == "user.created":
                # Lógica para usuário criado
                return {"success": True, "message": "User created successfully"}
            elif event_type == "user.updated":
                # Lógica para usuário atualizado
                return {"success": True, "message": "User updated successfully"}
            elif event_type == "user.deleted":
                # Lógica para usuário deletado
                return {"success": True, "message": "User deleted successfully"}
            else:
                return {
                    "success": False,
                    "error": f"Unsupported event type: {event_type}",
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
