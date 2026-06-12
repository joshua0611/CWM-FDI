from app.database.db import db


class DatabaseManager:
    """A class to manage SQLAlchemy database operations."""

    def __init__(self):
        self.db = db.session

    def create_user(self, username, password):
        """Create a new user with a hashed password."""
        from app.models import User

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, username, password):
        """Retrieve a user by username and verify the password."""
        from app.models import User

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    def get_user_by_username(self, username):
        """Retrieve a user by username"""
        from app.models import User

        return User.query.filter_by(username=username).first()

    def add_product(
        self, title, price, description, category_id, seller_id, image_url=None
    ):
        """Add a new product to the database."""
        from app.models import Product

        product = Product(
            title=title,
            price=price,
            description=description,
            category_id=category_id,
            seller_id=seller_id,
            image_url=image_url,
        )
        db.session.add(product)
        db.session.commit()
        return product

    def update_product(
        self,
        product_id,
        title=None,
        price=None,
        description=None,
        category_id=None,
        image_url=None,
    ):
        """Update an existing product in the database."""
        from app.models import Product

        product = Product.query.get(product_id)
        if product:
            # Update attributes if new values are provided (not None)
            if title:
                product.title = title
            if price is not None:
                product.price = price
            if description:
                product.description = description
            if category_id is not None:
                product.category_id = category_id
            if image_url:
                product.image_url = image_url
            db.session.commit()
            return product
        else:
            return None

    def delete_product(self, product_id):
        from app.models import Product, Cart

        try:
            product = Product.query.get(product_id)
            if product:
                Cart.query.filter_by(product_id=product_id).delete()
                db.session.delete(product)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            raise e

    def get_product_by_id(self, product_id):
        """Get product by ID."""
        from app.models import Product

        return Product.query.get(product_id)

    def get_products_by_seller_id(self, seller_id):
        """
        Get all products by a specific seller ID.
        """
        from app.models import Product

        return Product.query.filter_by(seller_id=seller_id).all()

    def get_all_categories(self):
        """Get all categories."""
        from app.models import Category

        return Category.query.all()

    def add_to_cart(self, user_id, product_id):
        """Add a product to a user's cart."""
        from app.models import Cart

        cart_item = Cart(user_id=user_id, product_id=product_id)
        db.session.add(cart_item)
        db.session.commit()

    def get_cart_items(self, user_id):
        """Retrieve all items in a user's cart using SQLAlchemy ORM."""

        from app.models import Cart, Product

        cart_items = (
            self.db.query(Cart, Product)
            .join(Product)
            .filter(Cart.user_id == user_id)
            .all()
        )

        return [
            {
                "title": cart_item.Product.title,
                "price": cart_item.Product.price,
                "image_url": cart_item.Product.image_url,
                "product_id": cart_item.Product.id,
            }
            for cart_item in cart_items
        ]

    def remove_from_cart(self, user_id, product_id):
        """Remove a product from the user's cart."""
        from app.models import Cart

        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()

    def get_all_products(self, page=1, per_page=5):
        """Retrieve all products with pagination."""
        from app.models import Product

        products_query = Product.query.paginate(
            page=page, per_page=per_page, error_out=False
        )  # Fetch products with pagination

        products = products_query.items
        total_products = products_query.total

        return {
            "products": [
                {
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                    "description": product.description,
                    "image_url": product.image_url,
                    "category_id": product.category_id,
                    "seller_id": product.seller_id,
                }
                for product in products
            ],
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_products": total_products,
                "total_pages": (total_products + per_page - 1) // per_page,
            },
        }

    def search_products(self, search_text, selected_categories, page=1, per_page=8):
        """Search for products by title, description, and category with pagination."""
        from app.models import Product
        from sqlalchemy import or_

        # Build the base query
        query = Product.query

        # Apply search filters for title and description using 'like'
        query = query.filter(
            or_(
                Product.title.like(f"%{search_text}%"),
                Product.description.like(f"%{search_text}%"),
            )
        )

        # Apply category filter if selected_categories are provided
        if selected_categories:
            query = query.filter(Product.category_id.in_(selected_categories))

        # Paginate the results
        products_query = query.paginate(page=page, per_page=per_page, error_out=False)
        products = products_query.items
        total_products = products_query.total

        # Returning the result with pagination details
        return {
            "products": [
                {
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                    "description": product.description,
                    "category": product.category.name,  # Assuming category is a relationship
                    "seller_id": product.seller_id,
                    "image_url": product.image_url,
                    "category_id": product.category_id,
                }
                for product in products
            ],
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_products": total_products,
                "total_pages": (total_products + per_page - 1) // per_page,
            },
        }

    def cart_item_exists(self, user_id, product_id):
        """Check if a specific product is in a user's cart."""
        from app.models import Cart

        # Using SQLAlchemy query to check if a product is in the user's cart
        cart_item = (
            db.session.query(Cart)
            .filter(Cart.user_id == user_id, Cart.product_id == product_id)
            .first()
        )

        # If cart_item is None, it means the product is not in the cart
        return cart_item is not None

    def get_total_cart_items(self, user_id):
        """Get the total number of items in a user's cart."""
        from app.models import Cart

        # Using SQLAlchemy to count the number of cart items for the given user
        total_items = db.session.query(Cart).filter(Cart.user_id == user_id).count()

        return total_items

    def get_products_by_category(self, category_id):
        """Retrieve all products that belong to a specific category."""
        from app.models import Product

        # Using SQLAlchemy to query products by category
        products = (
            db.session.query(Product).filter(Product.category_id == category_id).all()
        )
        return products
