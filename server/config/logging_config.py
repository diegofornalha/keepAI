import logging
from logging.handlers import RotatingFileHandler

from .settings import LOG_LEVEL, LOG_FORMAT, LOG_DIR


def setup_logging(app_name: str = "keepai") -> logging.Logger:
    """Configura o logging da aplicação."""

    # Cria o logger
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

    # Formata as mensagens
    formatter = logging.Formatter(LOG_FORMAT)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo
    log_file = LOG_DIR / f"{app_name}.log"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10_000_000, backupCount=5  # 10MB
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Logger global
logger = setup_logging()

__all__ = ["logger", "setup_logging"]
