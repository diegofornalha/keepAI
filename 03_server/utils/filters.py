from datetime import datetime
from typing import Union, Optional
from flask import Flask


def format_datetime(value: Optional[Union[str, datetime]]) -> str:
    """Formata uma string ISO 8601 para um formato mais amigável"""
    if not value:
        return ""
    try:
        if isinstance(value, str):
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            dt = value
        return dt.strftime("%d/%m/%Y %H:%M")
    except (ValueError, AttributeError):
        return str(value)


def register_filters(app: Flask) -> None:
    """Registra os filtros personalizados no app Flask"""
    app.jinja_env.filters["datetime"] = format_datetime
