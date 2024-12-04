from flask import render_template
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from app.models import Candle, Category

admin.add_view(ModelView(Candle, db.session))
admin.add_view(ModelView(Category, db.session))

@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(categories=categories)

@app.route('/')
def home():
    candles = Candle.query.all()
    return render_template('home.html', candles=candles)

@app.route('/category/<int:category_id>')
def category_page(category_id):
    # Fetch the category and its candles from the database
    category = Category.query.get_or_404(category_id)
    candles = category.candles  # Get all candles in this category
    return render_template('category.html', category=category, candles=candles)

    