from app.database.db import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default="EUR")
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True
    )
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    category = db.relationship("Category", backref="products")
    seller = db.relationship("User", backref="products")
