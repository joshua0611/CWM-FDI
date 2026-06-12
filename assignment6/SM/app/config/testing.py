# app/config/testing.py

from .config import Config


class TestingConfig(Config):
    """Testing-specific configuration settings."""

    # Database URI for testing (using SQLite in testing)
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"

    # Enable testing mode in Flask
    DEBUG = True
    TESTING = True

    # Disable modification tracking for SQLAlchemy in testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False
