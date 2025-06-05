"""
Configuration package for the Waste Management Intelligence System.
Single Responsibility: Application configuration management.
"""

from .settings import get_settings
from .database import get_session, create_db_and_tables, close_db
from .logging import setup_logging

__all__ = [
    "get_settings",
    "get_session", 
    "create_db_and_tables",
    "close_db",
    "setup_logging",
]