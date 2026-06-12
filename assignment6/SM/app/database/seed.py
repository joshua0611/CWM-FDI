from app.database.db import db


def insert_test_users():
    from app.models.user import User

    """Insert at least 3 test users with hashed passwords if they do not already exist."""
    test_users = [
        ("testuser1", "password1"),
        ("testuser2", "password2"),
        ("testuser3", "password3"),
    ]

    for username, password in test_users:
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)

    db.session.commit()


def insert_categories():
    from app.models.category import Category

    """Insert predefined categories if they do not already exist."""
    categories = [
        "Electronics",
        "Accessories",
        "Clothing",
        "Home & Kitchen",
        "Books",
        "Toys",
        "Sports",
        "Beauty & Personal Care",
    ]

    for category_name in categories:
        existing_category = Category.query.filter_by(name=category_name).first()
        if not existing_category:
            new_category = Category(name=category_name)
            db.session.add(new_category)

    db.session.commit()


def insert_sample_products():
    from app.models.product import Product

    """Insert a list of sample used products into the database with seller_id always 2 or 3."""
    sample_products = [
        (
            "Dell Inspiron 15 - Used Laptop, Great Condition",
            450.00,
            "EUR",
            "This pre-owned Dell Inspiron 15 laptop is in excellent working condition, perfect for students, professionals, or casual users. Equipped with a powerful processor, ample storage, and a long-lasting battery, it ensures smooth multitasking and efficient performance. The laptop has been well-maintained with minimal signs of wear, making it a budget-friendly alternative to a brand-new device. Whether for work, entertainment, or everyday tasks, this laptop is a reliable choice.",
            1,
            2,
            "/static/images/samples/laptop.webp",
        ),
        (
            "Apple iPhone 11 - Gently Used, Unlocked",
            350.00,
            "EUR",
            "Upgrade to this pre-owned iPhone 11, fully functional and unlocked for any carrier. This device has been gently used and is in good condition, with a vibrant Liquid Retina HD display, powerful A13 Bionic chip, and excellent battery life. It comes with a high-quality camera system, allowing you to capture stunning photos and 4K videos. Ideal for those looking for a premium smartphone at a fraction of the cost of a new one.",
            1,
            3,
            "/static/images/samples/iphone.webp",
        ),
        (
            "Bose QuietComfort 35 - Wireless Noise-Canceling Headphones",
            120.00,
            "EUR",
            "Immerse yourself in high-quality sound with these pre-owned Bose QC35 wireless headphones. Featuring world-class noise cancellation, they allow you to focus on your music, work, or calls without distractions. The soft ear cushions ensure all-day comfort, while the long battery life keeps you going for hours. Ideal for travelers, remote workers, or anyone who appreciates premium sound quality at an affordable price.",
            2,
            2,
            "/static/images/samples/headphone.webp",
        ),
        (
            "Fitbit Versa - Smart Fitness Watch with Heart Rate Monitor",
            80.00,
            "EUR",
            "This used Fitbit Versa smartwatch is perfect for tracking your fitness goals, monitoring heart rate, and staying connected on the go. With built-in activity tracking, sleep monitoring, and smartphone notifications, it’s the ultimate companion for a healthy lifestyle. The watch is in great condition, with a responsive touchscreen, comfortable strap, and long battery life. A budget-friendly way to stay active and organized.",
            2,
            3,
            "/static/images/samples/watch.webp",
        ),
        (
            "Men’s Genuine Leather Jacket - Pre-Owned, Stylish & Durable",
            60.00,
            "EUR",
            "Upgrade your wardrobe with this classic men’s leather jacket, crafted from genuine leather for a rugged yet stylish look. This pre-owned jacket has been well-kept, offering both warmth and durability. Featuring a comfortable fit and timeless design, it pairs well with casual and semi-formal outfits. Perfect for those who appreciate quality fashion without breaking the bank.",
            3,
            2,
            "/static/images/samples/jacket.webp",
        ),
        (
            "Graphic Print Cotton T-Shirt - Casual Wear, Used",
            10.00,
            "EUR",
            "This stylish graphic print t-shirt is made from breathable cotton, offering a soft and comfortable fit. Pre-owned but in good condition, it features a modern design that pairs well with jeans, shorts, or joggers. Whether for everyday casual wear or lounging at home, this affordable t-shirt is a great addition to your wardrobe.",
            3,
            3,
            "/static/images/samples/tshirt.webp",
        ),
        (
            "Philips High-Speed Blender - Pre-Owned, Works Perfectly",
            25.00,
            "EUR",
            "This used Philips blender is in excellent working condition, making it easy to prepare smoothies, shakes, soups, and sauces. With durable stainless steel blades and multiple speed settings, it ensures smooth blending for all your kitchen needs. The compact design fits well on any countertop, and it’s easy to clean after use. An ideal choice for budget-conscious home cooks.",
            4,
            2,
            "/static/images/samples/blender.webp",
        ),
        (
            "Nespresso Espresso Coffee Maker - Used, Fully Functional",
            50.00,
            "EUR",
            "Enjoy barista-quality coffee at home with this pre-owned Nespresso espresso machine. It’s in great condition and fully functional, delivering rich and aromatic coffee with the press of a button. Compact and stylish, this machine is easy to use and fits perfectly in any kitchen. Ideal for coffee lovers looking for a high-quality machine without the hefty price tag.",
            4,
            3,
            "/static/images/samples/coffee_maker.webp",
        ),
        (
            "Python Programming for Beginners - Used Book",
            15.00,
            "EUR",
            "This well-maintained book is an excellent introduction to Python programming, perfect for beginners and aspiring developers. Covering fundamental concepts, hands-on exercises, and real-world examples, it helps readers gain confidence in coding. If you’re looking to start a career in tech or improve your programming skills, this affordable used book is a great resource.",
            5,
            2,
            "/static/images/samples/python_book.webp",
        ),
        (
            "Data Science Essentials - Second-Hand Book, Like New",
            20.00,
            "EUR",
            "Expand your knowledge with this second-hand book on data science basics. Covering key topics such as machine learning, data analysis, and visualization, this book is perfect for students, professionals, and tech enthusiasts. It’s in excellent condition, with no missing pages or major wear. Get high-quality learning material at a lower price.",
            5,
            3,
            "/static/images/samples/data_science_book.webp",
        ),
        (
            "Women's Stylish Mini Dress - Pre-Owned, Cute & Comfortable",
            35.00,
            "EUR",
            "Refresh your wardrobe with this chic pre-owned mini dress. Crafted from soft, breathable fabric, it features a flattering fit and stylish design. Perfect for casual outings, date nights, or summer events. Its lightweight feel and modern cut make it a versatile go-to piece for any occasion — all at a budget-friendly price.",
            3,
            1,
            "/static/images/samples/mini_dress.webp",
        ),
        (
            "Classic Ceramic Coffee Mug - Durable & Stylish",
            12.00,
            "EUR",
            "This ceramic coffee mug is perfect for enjoying your favorite drinks. It has a classic design with a comfortable handle and is made from durable ceramic. It's gently used but still in great condition and ideal for everyday use. A great way to add a bit of style to your morning routine without spending too much.",
            4,
            1,
            "/static/images/samples/coffee_mug.webp",
        ),
        (
            "Non-Stick Frying Pan - High-Quality & Versatile",
            25.00,
            "EUR",
            "This non-stick frying pan is perfect for cooking all your favorite meals. It heats evenly and is easy to clean thanks to its non-stick surface. Though gently used, it's still in great shape and works well for frying, sautéing, and more. A great deal for a high-quality kitchen essential.",
            4,
            1,
            "/static/images/samples/frying_pan.webp",
        ),
    ]

    for (
        title,
        price,
        currency,
        description,
        category_id,
        seller_id,
        image_url,
    ) in sample_products:
        existing_product = Product.query.filter_by(title=title).first()
        if not existing_product:
            new_product = Product(
                title=title,
                price=price,
                currency=currency,
                description=description,
                category_id=category_id,
                seller_id=seller_id,
                image_url=image_url,
            )
            db.session.add(new_product)

    db.session.commit()


def insert_db_samples():
    try:
        insert_test_users()
        insert_categories()
        insert_sample_products()
    except Exception as e:
        db.session.rollback()
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    insert_db_samples()
