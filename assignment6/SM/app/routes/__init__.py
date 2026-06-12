from .auth import auth_bp
from .cart import cart_bp
from .home import general_bp
from .product import product_bp


def init_routes(app):
    """Register all route Blueprints with the Flask app."""
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(general_bp, url_prefix="/")
    app.register_blueprint(product_bp, url_prefix="/product")
