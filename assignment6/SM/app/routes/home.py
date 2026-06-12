from flask import Blueprint, render_template, current_app
from app.utils.helpers import render_error_page


general_bp = Blueprint("general", __name__)


@general_bp.route("/")
def home():
    """
    Home route, fetches and displays products for the homepage.
    """
    try:
        db = current_app.db
        products = db.get_all_products(page=1, per_page=4)["products"]
        return render_template("index.html", products=products)
    except Exception as e:
        return render_error_page(e)


@general_bp.route("/contact")
def contact():
    """
    Displays the contact page with user information.
    """
    return render_template("contact.html")
