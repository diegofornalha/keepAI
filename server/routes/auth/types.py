from typing import TypeVar, Callable, Union
from flask import Request as FlaskRequest, Response


class AuthenticatedRequest(FlaskRequest):
    """Tipo personalizado para request com user_id"""

    user_id: str


# Tipo para funções decoradas com require_auth
AuthenticatedFunction = TypeVar(
    "AuthenticatedFunction",
    bound=Callable[..., Union[Response, tuple[Response, int], str]],
)
