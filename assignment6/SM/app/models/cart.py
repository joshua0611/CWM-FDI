from app.database.db import db


class Cart(db.Model):
    __tablename__ = "carts"

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True, index=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), primary_key=True, index=True
    )

    user = db.relationship("User", backref=db.backref("cart", lazy=True))
    product = db.relationship("Product", backref=db.backref("cart", lazy=True))
