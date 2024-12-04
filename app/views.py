from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from app.models import Candle, Category, User
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm, DeleteAccountForm

admin.add_view(ModelView(Candle, db.session))
admin.add_view(ModelView(Category, db.session))

# to make the categories available everywhere
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
    category = Category.query.get_or_404(category_id)
    candles = category.candles  # Get all candles in this category
    return render_template('category.html', category=category, candles=candles)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))    

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/product/<int:candle_id>')
def product(candle_id):
    # Fetch the candle from the database
    candle = Candle.query.get_or_404(candle_id)
    category = candle.categories[0]
    return render_template('product.html', candle=candle, category=category)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Current password is incorrect.', 'danger')
    return render_template('change_password.html', form=form)

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            db.session.delete(current_user)
            db.session.commit()
            
            flash("Your account has been successfully deleted.", "success")
            return redirect(url_for('home'))
        else:
            flash("Incorrect password. Please try again.", "danger")
    
    return render_template('delete.html', form=form)