from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from app.models import Candle, Category

admin.add_view(ModelView(Candle, db.session))
admin.add_view(ModelView(Category, db.session))

@app.route('/')
def index():
    return "Hello World!!!"
    