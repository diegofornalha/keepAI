from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    """Schema para usuário"""

    id: str
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None
    metadata: Optional[dict] = None


class TokenSchema(BaseModel):
    """Schema para token de autenticação"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserSchema


class WebhookSchema(BaseModel):
    """Schema para webhooks do Clerk"""

    type: str
    data: dict
    object: str
