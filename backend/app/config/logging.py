"""
Logging configuration only.
Single Responsibility: Logging setup and configuration.
"""

import logging
import logging.config
import sys
from typing import Dict, Any
from pathlib import Path

from .settings import get_settings

settings = get_settings()


def setup_logging() -> None:
    """
    Configure application logging.
    Single Responsibility: Logging configuration.
    """
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Logging configuration
    log_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "default",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": log_dir / "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": log_dir / "error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "app": {
                "level": "DEBUG" if settings.debug else "INFO",
                "handlers": ["console", "file", "error_file"],
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "level": "INFO" if settings.database_echo else "WARNING",
                "handlers": ["file"],
                "propagate": False,
            },
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    }
    
    # Apply logging configuration
    logging.config.dictConfig(log_config)
    
    # Get logger for this module
    logger = logging.getLogger("app.config.logging")
    logger.info(f"Logging configured for environment: {settings.environment}")
    logger.info(f"Log level: {'DEBUG' if settings.debug else 'INFO'}")
    logger.info(f"Log directory: {log_dir.absolute()}")