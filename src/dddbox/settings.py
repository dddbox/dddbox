import logging.config
import os
import sys

import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

with open(os.path.join(BASE_DIR, "config.yml")) as config_file:
    CONFIG = yaml.safe_load(config_file)

BG_COLOR = CONFIG["background_color"]
PRIMARY_FONT_COLOR = CONFIG["primary_font_color"]
BUTTON_BACKGROUD_COLOR = CONFIG["button_backgroud_color"]
BUTTON_BACKGROUD_SECONDARY_COLOR = CONFIG["button_backgroud_secondary_color"]
BUTTON_BACKGROUD_TERTIARY_COLOR = CONFIG["button_backgroud_tertiary_color"]
ICON_FILL_COLOR = CONFIG["icon_fill_color"]

PRIMARY_COLOR = "#c95624"
WIDGET_BG_COLOR = "#303030"
WIDGET_BG_COLOR_DARK = "#262626"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {processName} {threadName} {message}",
            "style": "{",
        },
        "simple": {"format": "{message}", "style": "{",},
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
        }
    },
}

logging.config.dictConfig(LOGGING)
