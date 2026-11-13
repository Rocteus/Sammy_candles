from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample product catalog for your luxury candle store
PRODUCTS = [
    {"id": 1, "name": "Midnight Orchid & Amber", "price": 32.00, "image": "candle1.jpg", "category": "Woody"},
    {"id": 2, "name": "Vanilla Cashmere & Smoke", "price": 28.00, "image": "candle2.jpg", "category": "Warm"},
    {"id": 3, "name": "Eucalyptus & White Sage", "price": 30.00, "image": "candle3.jpg", "category": "Fresh"},
    {"id": 4, "name": "Rosewater & Velvet Peony", "price": 34.00, "image": "candle4.jpg", "category": "Floral"}
]

@app.route('/')
def home():
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return render_template('index.html', cart_count=cart_count)

@app.route('/collection')
def collection():
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return render_template('collection.html', products=PRODUCTS, cart_count=cart_count)

@app.route('/quiz')
def quiz():
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return render_template('quiz.html', cart_count=cart_count)

@app.route('/about')
def about():
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return render_template('about.html', cart_count=cart_count)

@app.route('/contact')
def contact():
    cart = session.get('cart', {})
    cart_count = sum(cart.values())
    return render_template('contact.html', cart_count=cart_count)

@app.route('/bag')
def bag():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            total_price += item_total
            cart_items.append({"product": product, "quantity": quantity, "total": item_total})
    cart_count = sum(cart.values())
    return render_template('bag.html', cart_items=cart_items, total_price=total_price, cart_count=cart_count)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('bag'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = next((p for p in PRODUCTS if p['id'] == int(product_id)), None)
        if product:
            item_total = product['price'] * quantity
            total_price += item_total
            cart_items.append({"product": product, "quantity": quantity, "total": item_total})
    cart_count = sum(cart.values())
    
    if request.method == 'POST':
        session.pop('cart', None)
        return redirect(url_for('thank_you'))
        
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price, cart_count=cart_count)

@app.route('/thank-you')
def thank_you():
    cart_count = 0
    return render_template('thank_you.html', cart_count=cart_count)

if __name__ == '__main__':
    app.run(debug=True)