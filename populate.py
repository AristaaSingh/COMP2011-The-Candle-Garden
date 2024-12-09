from app import app, db
from app.models import Candle, Category


with app.app_context():
    # categories
    fruity = Category(name="Fresh Fruity")
    herbs_fleurs = Category(name="Herbs & Fleurs")
    cozy_festive = Category(name="Cozy Festive")

    # 'Fresh Fruity' candles
    fruity_candles = [
        Candle(
            name="Strawberry Bliss",
            description="A delightful strawberry-scented candle to brighten your mood.",
            price=8.99,
            stock=10,
            image_filename="strawberry_bliss.jpg",
            categories=[fruity]
        ),
        Candle(
            name="Citrus Sunrise",
            description="A zesty orange and lemon candle to kickstart your day.",
            price=7.99,
            stock=15,
            image_filename="citrus_sunrise.jpg",
            categories=[fruity]
        ),
        Candle(
            name="Berry Burst",
            description="A juicy mixed berries candle for a sweet aroma.",
            price=12.49,
            stock=8,
            image_filename="berry_burst.jpg",
            categories=[fruity]
        ),
        Candle(
            name="Tropical Paradise",
            description="A coconut and pineapple candle for vacation vibes.",
            price=15.99,
            stock=12,
            image_filename="tropical_paradise.jpg",
            categories=[fruity]
        ),
        Candle(
            name="Apple Orchard",
            description="A crisp apple-scented candle for a refreshing feel.",
            price=11.99,
            stock=20,
            image_filename="apple_orchard.jpg",
            categories=[fruity]
        ),
        Candle(
            name="Peach Perfection",
            description="A luscious peach candle for a summery scent.",
            price=13.49,
            stock=18,
            image_filename="peach_perfection.jpg",
            categories=[fruity]
        )
    ]

    # 'Herbs & Fleurs' candles
    herbs_fleurs_candles = [
        Candle(
            name="Lavender Fields",
            description="A soothing lavender-scented candle for relaxation.",
            price=14.99,
            stock=15,
            image_filename="lavender_fields.jpg",
            categories=[herbs_fleurs]
        ),
        Candle(
            name="Rose Garden",
            description="A romantic rose-scented candle for a touch of elegance.",
            price=16.99,
            stock=10,
            image_filename="rose_garden.jpg",
            categories=[herbs_fleurs]
        ),
        Candle(
            name="Eucalyptus Fresh",
            description="A refreshing eucalyptus candle for a calming atmosphere.",
            price=12.99,
            stock=20,
            image_filename="eucalyptus_fresh.jpg",
            categories=[herbs_fleurs]
        ),
        Candle(
            name="Mint Melody",
            description="A crisp mint candle to invigorate your senses.",
            price=11.99,
            stock=25,
            image_filename="mint_melody.jpg",
            categories=[herbs_fleurs]
        ),
        Candle(
            name="Chamomile Calm",
            description="A soothing chamomile candle to help you unwind.",
            price=13.99,
            stock=12,
            image_filename="chamomile_calm.jpg",
            categories=[herbs_fleurs]
        ),
        Candle(
            name="Garden Sage",
            description="A herbaceous sage candle for a natural vibe.",
            price=12.49,
            stock=18,
            image_filename="garden_sage.jpg",
            categories=[herbs_fleurs]
        )
    ]

    # 'Cozy Festive' candles
    cozy_festive_candles = [
        Candle(
            name="Cinnamon Delight",
            description="A warm cinnamon candle for festive cheer.",
            price=14.99,
            stock=15,
            image_filename="cinnamon_delight.jpg",
            categories=[cozy_festive]
        ),
        Candle(
            name="Pumpkin Spice",
            description="A pumpkin spice candle to set the autumn mood.",
            price=13.99,
            stock=20,
            image_filename="pumpkin_spice.jpg",
            categories=[cozy_festive]
        ),
        Candle(
            name="Winter Wonderland",
            description="A crisp snow-inspired candle for cozy winter nights.",
            price=15.99,
            stock=10,
            image_filename="winter_wonderland.jpg",
            categories=[cozy_festive]
        ),
        Candle(
            name="Gingerbread Glow",
            description="A sweet gingerbread candle to fill your space with warmth.",
            price=12.99,
            stock=18,
            image_filename="gingerbread_glow.jpg",
            categories=[cozy_festive]
        ),
        Candle(
            name="Evergreen Forest",
            description="A fresh pine-scented candle for holiday vibes.",
            price=14.49,
            stock=15,
            image_filename="evergreen_forest.jpg",
            categories=[cozy_festive]
        ),
        Candle(
            name="Vanilla Cozy",
            description="A creamy vanilla candle for a comforting ambiance.",
            price=11.99,
            stock=22,
            image_filename="vanilla_cozy.jpg",
            categories=[cozy_festive]
        )
    ]

    # Aadddd categories and candles to database
    db.session.add_all([fruity, herbs_fleurs, cozy_festive])
    db.session.add_all(fruity_candles)
    db.session.add_all(herbs_fleurs_candles)
    db.session.add_all(cozy_festive_candles)

    db.session.commit()

    print("Database populated with real stock successfully!")
