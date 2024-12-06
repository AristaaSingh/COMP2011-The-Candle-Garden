from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from app.models import Candle, Category, User, Basket, BasketItem, Order, OrderItem
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm, DeleteAccountForm, CSRFProtectForm


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
    form = CSRFProtectForm()
    return render_template('home.html', candles=candles, form=form)

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
    form = DeleteAccountForm()
    return render_template('account.html', form=form)

@app.route('/product/<int:candle_id>')
def product(candle_id):
    candle = Candle.query.get_or_404(candle_id)
    form = CSRFProtectForm()
    category = candle.categories[0]
    return render_template('product.html', candle=candle, category=category, form=form)

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

@app.route('/add_to_basket/<int:candle_id>', methods=['POST'])
@login_required
def add_to_basket(candle_id):
    candle = Candle.query.get_or_404(candle_id)
    quantity = int(request.form.get('quantity', 1))  # Default to 1 if not specified

    if not current_user.basket:
        # Create a basket for the user if it doesn't exist
        basket = Basket(user=current_user)
        db.session.add(basket)
        db.session.commit()

    # Check if the item already exists in the basket
    item = next((item for item in current_user.basket.items if item.candle_id == candle.id), None)
    if item:
        # Update quantity if it exists
        item.quantity += quantity
    else:
        # Add new item if it doesn't exist
        new_item = BasketItem(basket=current_user.basket, candle=candle, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()

    flash(f"Added {quantity} of {candle.name} to your basket!", "success")
    return redirect(request.referrer or url_for('home'))


@app.route('/remove_from_basket/<int:candle_id>', methods=['POST'])
@login_required
def remove_from_basket(candle_id):
    candle = Candle.query.get_or_404(candle_id)

    if current_user.basket:
        # Find the item in the basket
        item = next((item for item in current_user.basket.items if item.candle_id == candle.id), None)
        if item:
            db.session.delete(item)  # Remove the item from the basket
            db.session.commit()
            flash(f"{candle.name} removed from your basket.", "info")

    return redirect(url_for('basket'))

@app.route('/basket')
@login_required
def basket():
    form = CSRFProtectForm()
    items = current_user.basket.items if current_user.basket else []
    total_price = sum(item.candle.price * item.quantity for item in items)
    return render_template('basket.html', items=items, total_price=total_price, form=form)

@app.route('/update_basket', methods=['POST'])
@login_required
def update_basket():
    """Update the basket quantity for a specific candle."""
    data = request.get_json()  # Get JSON data from the frontend
    item_id = data.get('item_id')  # Extract the BasketItem ID
    action = data.get('action')  # Extract the action (increment/decrement)

    item = BasketItem.query.get_or_404(item_id)
    if item.basket.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 403

    # Process the action
    if action == 'increment':
        item.quantity += 1
    elif action == 'decrement' and item.quantity > 1:
        item.quantity -= 1
    elif action == 'remove' or (action == 'decrement' and item.quantity == 1):
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            'success': True,
            'quantity': 0,  # Item removed
            'item_total': 0,  # No price if removed
            'basket_total': sum(i.candle.price * i.quantity for i in current_user.basket.items)
        })

    db.session.commit()

    # Calculate totals
    item_total = item.candle.price * item.quantity
    basket_total = sum(i.candle.price * i.quantity for i in current_user.basket.items)

    return jsonify({
        'success': True,
        'quantity': item.quantity,
        'item_total': item_total,
        'basket_total': basket_total
    })


@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    if not current_user.basket or not current_user.basket.items:
        flash('Your basket is empty.', 'danger')
        return redirect(url_for('basket'))

    # Check stock availability
    for item in current_user.basket.items:
        if item.quantity > item.candle.stock:
            flash(f"Insufficient stock for {item.candle.name}. Available: {item.candle.stock}", 'danger')
            return redirect(url_for('basket'))

    # Deduct stock and record the order
    total_price = 0
    for item in current_user.basket.items:
        candle = item.candle
        candle.stock -= item.quantity  # Deduct stock
        total_price += candle.price * item.quantity

    # Create an order
    order = Order(user=current_user, total_price=total_price)
    db.session.add(order)

    # Add items to the order
    for item in current_user.basket.items:
        order_item = OrderItem(
            order=order,
            candle=item.candle,
            quantity=item.quantity
        )
        db.session.add(order_item)
        db.session.delete(item)  # Clear basket items after checkout

    db.session.commit()

    flash('Checkout successful! Your order has been placed.', 'success')
    return redirect(url_for('account'))
