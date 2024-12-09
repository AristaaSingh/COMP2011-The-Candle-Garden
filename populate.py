from app import app, db
from app.models import Candle, Category

with app.app_context():
    # categories
    fruity = Category(name="Fresh Fruity")
    plant = Category(name="Herbs & Fleurs")
    festive = Category(name="Cozy Festive")

    candles = [
        # Cozy Festive
        Candle(
            name="The Elegant Reindeer",
            description="Exquisitely handcrafted, this unique deer carving is wild, graceful and sophisticated- all in one!",
            price=14.99,
            stock=50,
            image_filename="deer.jpg",
            image_reference="Mat, I. 2024. Cozy Green Candle Arrangement on Wooden Tray. [Online] [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/cozy-green-candle-arrangement-on-wooden-tray-29607858/",
            categories=[festive],
        ),
        Candle(
            name="Cranberry Cheer",
            description="Festive cranberry aroma to lift your spirits this holiday season!",
            price=13.99,
            stock=50,
            image_filename="cranberry.jpg",
            image_reference="Navarro, N. 2017. Red Lighted Candle. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/red-lighted-candle-714898/",
            categories=[festive],
        ),
        Candle(
            name="Reindeer Glow",
            description="Adorably handcrafted, this reindeer shines as bright as Rudolph’s famous nose!",
            price=15.99,
            stock=50,
            image_filename="reindeer.jpg",
            image_reference="Imre, A. 2022. Close up of Christmas Decorations and Wax Candle. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/close-up-of-christmas-decorations-and-wax-candle-14522919/",
            categories=[festive],
        ),
        Candle(
            name="Christmas Magic",
            description="Handcrafted with festive cheer, this tree-shaped candle sparkles with holiday charm!",
            price=16.99,
            stock=50,
            image_filename="tree.jpg",
            image_reference="Mat, I. 2024. Pink Christmas Tree Candle with Festive Decor. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/pink-christmas-tree-candle-with-festive-decor-29600749/",
            categories=[festive],
        ),
        Candle(
            name="Cinnamon Spice",
            description="Warm cinnamon scent perfect for cozy festive evenings in!",
            price=12.99,
            stock=50,
            image_filename="cinnamon.jpg",
            image_reference="Parache, A. 2021. A Bowl Of Food Sitting On Top Of A White Table. [Online]. [Accessed 7 December 2024]. Available from: https://unsplash.com/photos/a-bowl-of-food-sitting-on-top-of-a-white-table-NxT5a8T5dCA",
            categories=[festive],
        ),
        Candle(
            name="Mr Snowman",
            description="Knock, knock! Do you wanna build a snowman?",
            price=12.99,
            stock=50,
            image_filename="snowman.jpg",
            image_reference="Enache, M. 2024. Festive Snowman Candle with Evergreen Decor. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/festive-snowman-candle-with-evergreen-decor-29611437/",
            categories=[festive],
        ),
        # Fresh Fruity
        Candle(
            name="Bergamot Breeze",
            description="Citrusy bergamot notes for the refreshing and calming scent.",
            price=14.99,
            stock=50,
            image_filename="bergamot.jpg",
            image_reference="Svitlana. 2020. Red Candle On Brown Textile. [Online]. [Accessed 7 December 2024]. Available from: https://unsplash.com/photos/red-candle-on-brown-textile-lUZiv2LXsGw",
            categories=[fruity],
        ),
        Candle(
            name="Orange Zest",
            description="Your favourite classic- Bursting with fresh orange fragrance!",
            price=10.99,
            stock=50,
            image_filename="orange.jpg",
            image_reference="cottonbro studio. 2020. Sliced Orange Fruit Beside Squash. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/sliced-orange-fruit-beside-squash-5491148/",
            categories=[fruity],
        ),
        Candle(
            name="Grapfruit Burst",
            description="Sweet and tangy grapefruit, just the perfect scent to energise your day!",
            price=7.99,
            stock=50,
            image_filename="grape.jpg",
            image_reference="cocarinne. 2021. Burning aroma candle on books near grapefruit. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/burning-aroma-candle-on-books-near-grapefruit-7260252/",
            categories=[fruity],
        ),
        Candle(
            name="Green Apple Mischief",
            description="A crisp green apple aroma for a playful, candy like sweetness!",
            price=12.99,
            stock=50,
            image_filename="green.jpg",
            image_reference="Bolovtsova, K. Close up of Wax Candle. 2024. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/close-up-of-wax-candle-9130749/",
            categories=[fruity],
        ),
        Candle(
            name="Strawberry Dream",
            description="Creamy strawberry, now available as your favourite 'Short n Sweet' candle!",
            price=13.99,
            stock=50,
            image_filename="strawberry.jpg",
            image_reference="Parache, A. 2023. Dessert-inspired candle with strawberries. [Online]. [Accessed 7 December 2024]. Available from: https://unsplash.com/photos/a-cup-of-ice-cream-with-strawberries-on-top--HEUNeXZ_wM",
            categories=[fruity],
        ),
        Candle(
            name="Lemon Bliss",
            description="When life give you lemons, make a candle from them!",
            price=7.99,
            stock=50,
            image_filename="lemon.jpg",
            image_reference="Tikovka1355. Lemon candle, Scented candle, Blackberry candle image. 2021. [Online]. [Accessed 7 December 2024]. Available from: https://pixabay.com/photos/lemon-candle-scented-candle-6668364/",
            categories=[fruity],
        ),
        # Herbs & Fleurs
        Candle(
            name="Hydrangea Full Bloom",
            description="Whoa, did you smell a bouquet? Nope, it's just the Hydrangea Full Bloom - real fan favourite!",
            price=14.99,
            stock=50,
            image_filename="hydrangea.jpg",
            image_reference="NuvolaBianca. Candle, Table, Ornament image. 2017. [Online]. [Accessed 7 December 2024]. Available from: https://pixabay.com/photos/candle-table-ornament-wax-2140758/",
            categories=[plant],
        ),
        Candle(
            name="Lavender Fields",
            description="Whisk yourself away to dreamy lavender fields where the only thing blooming brighter is your charm!",
            price=15.99,
            stock=50,
            image_filename="lavender.jpg",
            image_reference="Vie Studio. 2021. A Candle in a Brown Glass Bottle. [Online]. [Accessed 7 December 2024]. Available from: https://www.pexels.com/photo/a-candle-in-a-brown-glass-bottle-7004671/",
            categories=[plant],
        ),
        Candle(
            name="Pine Forest",
            description="Fresh, crisp, and a little wild— that's our earthy Pine Forest candle scent!",
            price=16.99,
            stock=50,
            image_filename="pine.jpg",
            image_reference="Svitlana. 2020. Black and White Glass Container. [Online]. [Accessed 7 December 2024]. Available from: https://unsplash.com/photos/black-and-white-glass-container-fOSqP54S8So",
            categories=[plant],
        ),
        Candle(
            name="Lily, Lily",
            description="A playful pop of pink, as sweet and sassy as a lily!",
            price=13.99,
            stock=50,
            image_filename="lily.jpg",
            image_reference="debbieryan2009. Lily Flowers. 2017. [Online]. [Accessed 7 December 2024]. Available from: https://pixabay.com/photos/lillies-lily-flowers-floral-2082933/",
            categories=[plant],
        ),
        Candle(
            name="Sandalwood Serene",
            description="Earthy, warm, and endlessly soothing—serenity wrapped in sandalwood’s embrace.",
            price=7.99,
            stock=50,
            image_filename="sandalwood.jpg",
            image_reference="RYNA Studio. 2021. Clear Glass Jar with White Powder Inside. [Online]. [Accessed 7 December 2024]. Available from: https://unsplash.com/photos/clear-glass-jar-with-white-powder-inside-WYKbOj_J0LY",
            categories=[plant],
        ),
        Candle(
            name="Rose Petals",
            description="Soft, romantic, and utterly irresistible—like a love-letter written in rose petals!",
            price=10.99,
            stock=50,
            image_filename="rose.jpg",
            image_reference="monicore. 2019. Table candle decoration interior. [Online]. [Accessed 7 December 2024]. Available from: https://pixabay.com/photos/table-candle-decoration-interior-4222263/",
            categories=[plant],
        ),
    ]

    # Add categories to the database
    db.session.add(fruity)
    db.session.add(plant)
    db.session.add(festive)

    # Add candles to the database
    for candle in candles:
        db.session.add(candle)

    # Commit the changes
    db.session.commit()

    print("Database populated successfully with reordered stock!")