import os
import secrets


class Config:
    """Base configuration settings shared across all environments."""

    # Secret key for session management
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///default.db"  # Default DB, can be overridden by environment
    )

    # Session cookie settings
    SESSION_COOKIE_SECURE = True

    # File upload settings
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    ROOT_DIR = "app"
    DEFAULT_IMAGE_URL = "/static/images/no_image.jpg"
    IMAGE_UPLOAD_FOLDER = "static/images/uploads"
