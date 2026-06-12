from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
)
from app.utils.helpers import render_error_page, load_next_page
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    User login page.
    Handles login form submission and redirects to the homepage on success.
    """
    if request.method == "POST":
        try:
            db = current_app.db
            username = request.form["username"]
            password = request.form["password"]
            user = db.get_user(username, password)
            if user:
                session["total_cart_items"] = db.get_total_cart_items(user.id)
                login_user(user)
                return load_next_page(request)
            else:
                flash("Invalid username or password", "danger")
        except Exception as e:
            return render_error_page(e)
    return render_template("auth.html", is_login=True)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration page.
    Allows new users to register and redirects to login on success.
    """
    if request.method == "POST":
        try:
            db = current_app.db
            username = request.form["username"]
            password = request.form["password"]

            # Check if the username already exists in the database
            existing_user = db.get_user_by_username(username)

            if existing_user:
                flash(
                    "Username already exists. Please choose a different one.", "danger"
                )
                return redirect(url_for("auth.register"))

            db.create_user(username, password)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            return render_error_page(e)

    return render_template("auth.html", is_login=False)


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Logs out the user and clears session data.
    """
    session.clear()
    logout_user()
    return redirect(url_for("general.home"))
