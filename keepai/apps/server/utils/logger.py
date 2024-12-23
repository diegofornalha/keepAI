import atexit
import logging
import os
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler


def setup_logger():
    # Certifica que o diretório de logs existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configura o logger principal
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "simple": {"format": "%(message)s"},
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": os.path.join(log_dir, "keepai.log"),
                    "formatter": "default",
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5,
                },
                "console": {"class": "logging.StreamHandler", "formatter": "default"},
                "grpc": {
                    "class": "logging.FileHandler",
                    "filename": os.path.join(log_dir, "grpc.log"),
                    "formatter": "simple",
                },
            },
            "loggers": {
                "keepai": {
                    "level": "INFO",
                    "handlers": ["file", "console"],
                    "propagate": False,
                },
                "grpc": {"level": "WARNING", "handlers": ["grpc"], "propagate": False},
            },
            "root": {"level": "INFO", "handlers": ["file", "console"]},
        }
    )

    # Configura o logger do gRPC
    grpc_logger = logging.getLogger("grpc")
    grpc_logger.setLevel(logging.WARNING)

    # Registra função de cleanup
    def cleanup():
        # Fecha todos os handlers
        for handler in logging.getLogger("keepai").handlers:
            handler.close()
        for handler in grpc_logger.handlers:
            handler.close()

    atexit.register(cleanup)

    return logging.getLogger("keepai")
