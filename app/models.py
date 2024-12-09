from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# association Table for Many-to-Many Relationship between Candle and Category
candle_category = db.Table(
    'candle_category',
    db.Column('candle_id', db.Integer, db.ForeignKey('candle.id'),
              primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'),
              primary_key=True)
)

# association Table for Many-to-Many Relationship between Basket and Candle
basket_candle = db.Table(
    'basket_candle',
    db.Column('basket_id', db.Integer, db.ForeignKey('basket.id'),
              primary_key=True),
    db.Column('candle_id', db.Integer, db.ForeignKey('candle.id'),
              primary_key=True)
)


class Candle(db.Model):
    """Model for Candles"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_filename = db.Column(db.String(255), nullable=True)
    image_reference = db.Column(db.String(255), nullable=True)
    categories = db.relationship('Category', secondary=candle_category,
                                 back_populates='candles')
    baskets = db.relationship('Basket', secondary=basket_candle,
                              back_populates='candles')
    orders = db.relationship('OrderItem', back_populates='candle')

    def __repr__(self):
        return f"<Candle {self.name}>"


class Category(db.Model):
    """Model for Categories"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    candles = db.relationship('Candle', secondary=candle_category,
                              back_populates='categories')

    def __repr__(self):
        return f"<Category {self.name}>"


class User(UserMixin, db.Model):
    """Model for Users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', back_populates='user',
                             cascade='all, delete-orphan')
    basket = db.relationship('Basket', uselist=False, back_populates='user')
    addresses = db.relationship('Address', back_populates='user',
                                cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Address(db.Model):
    """Model for User Addresses"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address_line1 = db.Column(db.String(255), nullable=False)
    address_line2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', back_populates='addresses')

    def __repr__(self):
        return f"<Address {self.address_line1}, {self.city}>"


class Basket(db.Model):
    """Model for User's Basket"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='basket')
    candles = db.relationship('Candle', secondary=basket_candle,
                              back_populates='baskets')
    items = db.relationship('BasketItem', back_populates='basket',
                            cascade="all, delete-orphan")

    def add_candle(self, candle):
        if candle not in self.candles:
            self.candles.append(candle)

    def remove_candle(self, candle):
        if candle in self.candles:
            self.candles.remove(candle)

    def clear(self):
        self.candles.clear()

    def __repr__(self):
        return f"<Basket {self.id} - User {self.user.username}>"


class BasketItem(db.Model):
    """Model for items in the basket"""
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('basket.id'),
                          nullable=False)
    candle_id = db.Column(db.Integer, db.ForeignKey('candle.id'),
                          nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    basket = db.relationship('Basket', back_populates='items')
    candle = db.relationship('Candle')

    def __repr__(self):
        return f"<BasketItem {self.candle.name} x{self.quantity}>"


class Order(db.Model):
    """Model for Orders"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False,
                           default=db.func.current_timestamp())
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('address.id'),
                                    nullable=False)
    user = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order',
                            cascade='all, delete-orphan')
    delivery_address = db.relationship('Address')

    def __repr__(self):
        return f"<Order {self.id} - User {self.user.username}>"


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    candle_id = db.Column(db.Integer, db.ForeignKey('candle.id'),
                          nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    candle = db.relationship('Candle')
    order = db.relationship('Order', back_populates='items')

    def __repr__(self):
        return f"<OrderItem {self.candle.name} x{self.quantity}>"
