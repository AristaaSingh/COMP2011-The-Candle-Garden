from app import app, db
from app.models import Candle, Category

# Push the application context
with app.app_context():
    # Categories
    fruity = Category(name="Fruity")
    floral = Category(name="Floral")

    # Candles
    candle1 = Candle(
        name="Strawberry Bliss",
        description="A delightful strawberry-scented candle to brighten your mood.",
        price=12.99,
        stock=10,
        image_filename="candela.jpeg",
        categories=[fruity]
    )
    candle2 = Candle(
        name="Lavender Fields",
        description="A soothing lavender-scented candle for relaxation.",
        price=14.99,
        stock=15,
        image_filename="candela.jpeg",
        categories=[floral]
    )

    # Add items to the database
    db.session.add(fruity)
    db.session.add(floral)
    db.session.add(candle1)
    db.session.add(candle2)

    # Commit the changes
    db.session.commit()

    print("Database populated successfully!")
