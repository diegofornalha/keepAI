from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    """Modelo para perfil de usuário."""

    id: UUID
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Configurações do modelo."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "image_url": "https://example.com/avatar.jpg",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            }
        }
