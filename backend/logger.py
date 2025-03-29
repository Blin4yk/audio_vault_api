import logging
import sys

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'generic_console': {
            'format': '%(asctime)s [%(levelname)s] %(message)s (%(name)s:%(filename)s:%(funcName)s:%(lineno)d)',
        },
        'generic_json': {
            'class': 'logs_utils.JsonFormatter',
            'datefmt': '%Y-%m-%d %H:%M:%S.%f',
        }
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic_console',
            'stream': sys.stdout,
        },
        'console_error': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic_console',
            'stream': sys.stderr,
            'level': 'ERROR',
        },
        'file': {
            'class': 'logs_utils.CustomTimedRotatingFileHandler',
            'formatter': 'generic_json',
            'filename': 'app.log',
            'when': 'midnight',
            'interval': 1,
            'encoding': 'utf-8',
            'datefmt': '%Y-%m-%d',
        }
    },
    loggers={
        'audio_vault': {
            'level': 'INFO',
            'handlers': ['console', 'console_error', 'file'],
            'propagate': False
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
        },
        'sqlalchemy': {
            'level': 'DEBUG',
            'propagate': True
        }

    }
)

logging.config.dictConfig(LOGGING_CONFIG)

backend_logger = logging.getLogger('audio_vault')
