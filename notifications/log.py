import logging.handlers

LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'critical': logging.CRITICAL
}

LOG_FORMAT = '%(asctime)s.%(msecs)03d  %(levelname)-8s  %(filename)-14s  %(message)s'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
MAX_BYTES = 10000000
BACKUP_COUNT = 1
LOG_LEVEL = logging.INFO
LOGFILE = 'notifications.log'


def configure_root_logger(filename, max_bytes=MAX_BYTES, backup_count=BACKUP_COUNT, level=LOG_LEVEL):
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(
        filename=filename, mode='a', maxBytes=max_bytes, backupCount=backup_count
    )
    logger.addHandler(handler)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATETIME_FORMAT)
    handler.setFormatter(formatter)
    return logger
