from .config import Config


class ProductionConfig(Config):
    """Production-specific configuration settings."""

    # Database URI for production (you would use a more robust DB like PostgreSQL or MySQL in production)
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///production.db"  # Change to your production DB URI
    )

    # Disable debug mode in production
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # Cookies must be sent over HTTPS in production
