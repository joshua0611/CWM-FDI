# app/config/development.py

from .config import Config


class DevelopmentConfig(Config):
    """Development-specific configuration settings."""

    # Database URI for development (using SQLite in development)
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"

    # Enable Flask's debug mode
    DEBUG = True
    TESTING = False
