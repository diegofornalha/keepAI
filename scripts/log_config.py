import logging
import logging.handlers
import os
from pythonjsonlogger import jsonlogger

def setup_logging():
    log_dir = os.getenv('LOG_DIR', '/app/logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configuração básica
    logger = logging.getLogger()
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    
    # Handler para arquivo com rotação
    log_file = f"{log_dir}/keepai.log"
    handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when=os.getenv('LOG_ROTATION_INTERVAL', 'D'),
        interval=1,
        backupCount=int(os.getenv('LOG_BACKUP_COUNT', 10))
    )
    
    # Formato JSON para logs
    if os.getenv('LOG_FORMAT') == 'json':
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger 