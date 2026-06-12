import os
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig


def get_config():
    """Get the appropriate configuration based on the environment."""
    env = os.getenv(
        "FLASK_ENV", "development"
    ).lower()  # Default to 'development' if FLASK_ENV is not set

    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig
