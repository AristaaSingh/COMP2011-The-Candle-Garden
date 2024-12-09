from flask import render_template, redirect, url_for, flash
from flask import request, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from app.models import Candle, Category, User, Basket
from app.models import BasketItem, Order, OrderItem, Address
from app.forms import RegistrationForm, LoginForm, ChangePasswordForm
from app.forms import DeleteAccountForm, CSRFProtectForm, AddressForm


admin.add_view(ModelView(Candle, db.session))
admin.add_view(ModelView(Category, db.session))


# to make the categories available everywhere
@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(categories=categories)


# pages or display related routes
@app.route('/')
def home():
    candles = Candle.query.all()
    form = CSRFProtectForm()
    return render_template('home.html', candles=candles, form=form)


@app.route('/category/<int:category_id>')
def category_page(category_id):
    form = CSRFProtectForm()
    category = Category.query.get_or_404(category_id)
    candles = category.candles  # Get all candles in this category
    return render_template('category.html', category=category, candles=candles,
                           form=form)


@app.route('/product/<int:candle_id>')
def product(candle_id):
    candle = Candle.query.get_or_404(candle_id)
    form = CSRFProtectForm()
    category = candle.categories[0]
    return render_template('product.html', candle=candle, category=category,
                           form=form, candle_reference=candle.image_reference)


@app.route('/cookie-policy')
def cookie_policy():
    return render_template('cookie_policy.html')


@app.route('/search')
def search():
    form = CSRFProtectForm()
    query = request.args.get('query', '').strip()
    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('home'))
    # Search for candles by name or description
    results = Candle.query.filter(
        (Candle.name.ilike(f"%{query}%")) |
        (Candle.description.ilike(f"%{query}%")) |
        (Candle.categories.any(Category.name.ilike(f"%{query}%")))
    ).all()
    return render_template('search_results.html', query=query,
    results=results, form=form)


# account related routes
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
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your email and password.',
                  'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
def account():
    """Account management and address handling."""
    form = DeleteAccountForm()
    address_form = AddressForm()
    # for new address submission
    if address_form.validate_on_submit():
        address = Address(
            user=current_user,
            address_line1=address_form.address_line1.data,
            address_line2=address_form.address_line2.data,
            city=address_form.city.data,
            state=address_form.state.data,
            postal_code=address_form.postal_code.data,
            country=address_form.country.data
        )
        db.session.add(address)
        db.session.commit()
        flash("Address added successfully!", "success")
        return redirect(url_for('account'))
    return render_template('account.html', form=form,
                           address_form=address_form)


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


@app.route('/addresses', methods=['GET', 'POST'])
@login_required
def addresses():
    form = AddressForm()
    if form.validate_on_submit():
        address = Address(
            user=current_user,
            address_line1=form.address_line1.data,
            address_line2=form.address_line2.data,
            city=form.city.data,
            state=form.state.data,
            postal_code=form.postal_code.data,
            country=form.country.data
        )
        db.session.add(address)
        db.session.commit()
        flash('Address saved successfully!', 'success')
        return redirect(url_for('addresses'))
    return render_template('addresses.html', form=form,
                           addresses=current_user.addresses)


@app.route('/remove_address/<int:address_id>', methods=['POST'])
@login_required
def remove_address(address_id):
    """Remove an address."""
    address = Address.query.get_or_404(address_id)
    if address.user_id != current_user.id:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('account'))
    db.session.delete(address)
    db.session.commit()
    flash("Address removed successfully.", "success")
    return redirect(url_for('account'))


# basket related routes
@app.route('/add_to_basket/<int:candle_id>', methods=['POST'])
@login_required
def add_to_basket(candle_id):
    candle = Candle.query.get_or_404(candle_id)
    quantity = int(request.form.get('quantity', 1))
    if not current_user.basket:
        # create basket instance if it doesnt exist
        basket = Basket(user=current_user)
        db.session.add(basket)
        db.session.commit()
    # increase qantity if item already exists in basket
    item = next((item for item in current_user.basket.items if
                 item.candle_id == candle.id), None)
    if item:
        item.quantity += quantity
    else:
        # new item if it didnt already exist
        new_item = BasketItem(basket=current_user.basket, candle=candle,
                              quantity=quantity)
        db.session.add(new_item)
    db.session.commit()
    flash(f"Added {quantity} of {candle.name} to your basket!", "success")
    return redirect(request.referrer or url_for('home'))


@app.route('/remove_from_basket/<int:candle_id>', methods=['POST'])
@login_required
def remove_from_basket(candle_id):
    candle = Candle.query.get_or_404(candle_id)
    if current_user.basket:
        item = next((item for item in current_user.basket.items if
                     item.candle_id == candle.id), None)
        if item:
            db.session.delete(item)
            db.session.commit()
            flash(f"{candle.name} removed from your basket.", "info")
    return redirect(url_for('basket'))


@app.route('/basket')
@login_required
def basket():
    form = CSRFProtectForm()
    items = current_user.basket.items if current_user.basket else []
    total_price = sum(item.candle.price * item.quantity for item in items)
    return render_template('basket.html', items=items, total_price=total_price,
                           form=form)


@app.route('/update_basket', methods=['POST'])
@login_required
def update_basket():
    """Update the basket quantity for a specific candle."""
    data = request.get_json()
    item_id = data.get('item_id')
    action = data.get('action')
    item = BasketItem.query.get_or_404(item_id)
    if item.basket.user_id != current_user.id:
        return jsonify(
            {'success': False, 'message': 'Unauthorized access'}), 403
    # process the action
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
            'basket_total': sum(i.candle.price * i.quantity for i in
                                current_user.basket.items)
        })
    db.session.commit()
    # calculate totals
    item_total = item.candle.price * item.quantity
    basket_total = sum(i.candle.price * i.quantity for i in
                       current_user.basket.items)
    return jsonify({
        'success': True,
        'quantity': item.quantity,
        'item_total': item_total,
        'basket_total': basket_total
    })


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page."""
    address_form = AddressForm()
    if request.method == 'POST':
        if not current_user.basket or not current_user.basket.items:
            flash('Your basket is empty.', 'danger')
            return redirect(url_for('basket'))
        # selected address or new address
        delivery_address_id = request.form.get('delivery_address_id')
        if delivery_address_id:
            delivery_address = Address.query.get(delivery_address_id)
        elif address_form.validate():
            delivery_address = Address(
                user=current_user,
                address_line1=address_form.address_line1.data,
                address_line2=address_form.address_line2.data,
                city=address_form.city.data,
                state=address_form.state.data,
                postal_code=address_form.postal_code.data,
                country=address_form.country.data,
            )
            db.session.add(delivery_address)
            db.session.commit()
        else:
            flash("Please select or add a valid delivery address.", "danger")
            return redirect(url_for('checkout'))
        # validate stock and place the order
        for item in current_user.basket.items:
            if item.quantity > item.candle.stock:
                flash(f"Insufficient stock for {item.candle.name}.", "danger")
                return redirect(url_for('basket'))
        total_price = sum(item.candle.price * item.quantity for item in
                          current_user.basket.items)
        order = Order(user=current_user, total_price=total_price,
                      delivery_address=delivery_address)
        db.session.add(order)
        for item in current_user.basket.items:
            db.session.add(OrderItem(order=order, candle=item.candle,
                                     quantity=item.quantity))
            item.candle.stock -= item.quantity
            db.session.delete(item)
        db.session.commit()
        flash("Checkout successful! Your order has been placed.", "success")
        return redirect(url_for('account'))
    return render_template(
        'checkout.html',
        addresses=current_user.addresses,
        address_form=address_form
    )
