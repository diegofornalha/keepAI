import logging
import logging.config
from typing import Dict, Any
from pythonjsonlogger import jsonlogger  # type: ignore


def setup_logging() -> None:
    """Configura o logging em formato JSON"""
    logger = logging.getLogger()
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
