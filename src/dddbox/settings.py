import logging.config
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {processName} {threadName} {message}",
            "style": "{",
        },
        "simple": {"format": "GCODE: {message}", "style": "{",},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": sys.stdout,
        },
        "simple_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "dddbox": {
            "handlers": ["console"],
            "propagate": False,
            "level": "INFO",
        },
        "dddbox.devices.gcode": {
            "handlers": ["simple_console"],
            "propagate": False,
            "level": "ERROR",
        },
    },
}

logging.config.dictConfig(LOGGING)
