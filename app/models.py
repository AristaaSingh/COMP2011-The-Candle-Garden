from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Association Table for Many-to-Many Relationship between Candle and Category
candle_category = db.Table(
    'candle_category',
    db.Column('candle_id', db.Integer, db.ForeignKey('candle.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Candle(db.Model):
    """Model for Candles"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    categories = db.relationship('Category', secondary=candle_category, back_populates='candles')

    def __repr__(self):
        return f"<Candle {self.name}>"

class Category(db.Model):
    """Model for Categories"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    candles = db.relationship('Candle', secondary=candle_category, back_populates='categories')

    def __repr__(self):
        return f"<Category {self.name}>"

class User(UserMixin, db.Model):
    """Model for Users"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Order(db.Model):
    """Model for Orders"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    user = db.relationship('User', back_populates='orders')
    candles = db.relationship('Candle', secondary='order_candle', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id} - User {self.user.username}>"

# Association Table for Many-to-Many Relationship between Order and Candle
order_candle = db.Table(
    'order_candle',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('candle_id', db.Integer, db.ForeignKey('candle.id'), primary_key=True)
)