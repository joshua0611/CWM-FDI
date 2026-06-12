from flask import Flask, session
from app.models.user import User
from app.config import get_config
from .routes import init_routes
from app.database.db import db, init_db
from app.database.seed import insert_db_samples
from app.database.manager import DatabaseManager
from flask_login import LoginManager, current_user


def create_app():
    app = Flask(__name__)

    # Load config from config folder
    app.config.from_object(get_config())

    # Initialize extensions
    init_db(app)

    app.db = DatabaseManager()

    login_manager = LoginManager()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_user():
        return {
            "user": current_user,
            "total_cart_items": session.get("total_cart_items", 0),
        }

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "You need to log in to access this page."
    login_manager.login_message_category = "warning"

    with app.app_context():
        db.create_all()

        # Check if the database is empty and insert sample data
        if db.session.query(db.exists().where(User.id == 1)).scalar() == False:
            insert_db_samples()

    init_routes(app)

    return app
