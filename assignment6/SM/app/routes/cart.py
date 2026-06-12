from flask import (
    Blueprint,
    redirect,
    url_for,
    session,
    current_app,
    render_template,
    request,
)
from app.utils import render_error_page
from flask_login import login_required, current_user

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/")
@login_required
def cart():
    """
    Displays the user's cart with items and total price.
    """
    try:
        db = current_app.db
        cart_items = db.get_cart_items(current_user.id)
        return render_template("cart.html", cart_items=cart_items)
    except Exception as e:
        return render_error_page(e)


@cart_bp.route("/add/<int:product_id>", methods=["GET", "POST"])
@login_required
def add_to_cart(product_id):
    """
    Adds a product to the cart and redirects to the product's page.
    """
    try:
        db = current_app.db
        added_to_cart = db.cart_item_exists(current_user.id, product_id)
        if added_to_cart:
            return redirect(url_for("product.view_product", product_id=product_id))

        product = db.get_product_by_id(product_id)
        if not product:
            return render_error_page("Product not found", 404)

        if product.seller_id != current_user.id:
            db.add_to_cart(current_user.id, product_id)
            session["total_cart_items"] = db.get_total_cart_items(current_user.id)

        return redirect(url_for("product.view_product", product_id=product_id))
    except Exception as e:
        return render_error_page(e)


@cart_bp.route("/remove/<int:product_id>", methods=["POST", "GET"])
@login_required
def remove_from_cart(product_id):
    """
    Removes a product from the cart and redirects to either cart or product page.
    """
    try:
        db = current_app.db
        if not db.cart_item_exists(current_user.id, product_id):
            return render_error_page("Cart item not found or unauthorized access", 404)

        db.remove_from_cart(current_user.id, product_id)
        session["total_cart_items"] = db.get_total_cart_items(current_user.id)
        if request.method == "POST":
            return redirect(url_for("cart.cart"))
        else:
            return redirect(url_for("product.view_product", product_id=product_id))
    except Exception as e:
        return render_error_page(e)
