import logging

from markdown_it.presets import default

from .base import *
from decouple import config, Csv

DEBUG = config("DEBUG", default=False, cast=bool)
JWT_COOKIE_SECURE = False
JWT_COOKIE_SAMESITE = "Lax"
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# Development CORS configuration
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())
# =============================================================================
# LOGGING
# =============================================================================

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] {name} | {funcName}:{lineno} | {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },

    "filters": {
        # DEBUG only
        "debug_only": {
            "()": "config.logging_filters.LevelRangeFilter",
            "min_level": logging.DEBUG,
            "max_level": logging.DEBUG,
        },

        # INFO + WARNING only
        "info_warning_only": {
            "()": "config.logging_filters.LevelRangeFilter",
            "min_level": logging.INFO,
            "max_level": logging.WARNING,
        },

        # ERROR + CRITICAL only
        "error_critical_only": {
            "()": "config.logging_filters.LevelRangeFilter",
            "min_level": logging.ERROR,
            "max_level": logging.CRITICAL,
        },
    },

    "handlers": {
        # -------------------------
        # Console
        # -------------------------

        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "stream": sys.stdout,
            "filters": ["info_warning_only"],
        },

        "console_error": {
            "class": "logging.StreamHandler",
            "level": "ERROR",
            "formatter": "verbose",
            "stream": sys.stderr,
            "filters": ["error_critical_only"],
        },

        # -------------------------
        # Debug file
        # -------------------------

        "debug_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "debug.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "level": "DEBUG",
            "filters": ["debug_only"],
            "encoding": "utf-8",
        },

        # -------------------------
        # Info file
        # -------------------------

        "info_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "info.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "level": "INFO",
            "filters": ["info_warning_only"],
            "encoding": "utf-8",
        },

        # -------------------------
        # Error file
        # -------------------------

        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "error.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 10,
            "formatter": "verbose",
            "level": "ERROR",
            "filters": ["error_critical_only"],
            "encoding": "utf-8",
        },
    },

    "root": {
        "handlers": [
            "console",
            "console_error",
        ],
        "level": "DEBUG",
    },

    "loggers": {
        "django": {
            "handlers": [
                "console",
                "console_error",
                "info_file",
                "error_file",
            ],
            "level": "INFO",
            "propagate": False,
        },

        "hrms": {
            "handlers": [
                "console",
                "console_error",
                "debug_file",
                "info_file",
                "error_file",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
