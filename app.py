from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'

PRODUCTS = [
    {
        "id": 1,
        "name": "Midnight Velvet",
        "tagline": "Deep, smoky, and sophisticated.",
        "notes": "Top: Black Fig, Cardamom | Heart: Amber, Tobacco Leaf | Base: Cedarwood, Dark Musk",
        "price": 28.00,
        "burn_time": "50+ Hours",
        "wax": "100% Organic Coconut-Soy Wax"
    },
    {
        "id": 2,
        "name": "Golden Saffron & Silk",
        "tagline": "Warm, luminous, and cocooning.",
        "notes": "Top: Saffron, White Tea | Heart: Orchid, Golden Amber | Base: Sandalwood, Vanilla Bean",
        "price": 30.00,
        "burn_time": "50+ Hours",
        "wax": "100% Organic Coconut-Soy Wax"
    },
    {
        "id": 3,
        "name": "Amethyst Cashmere",
        "tagline": "Soft, floral, and effortlessly clean.",
        "notes": "Top: Bergamot, Lavender Blossom | Heart: Cashmere Musk, Violet Leaf | Base: White Amber",
        "price": 28.00,
        "burn_time": "50+ Hours",
        "wax": "100% Organic Coconut-Soy Wax"
    }
]

@app.route('/')
def home():
    cart_count = len(session.get('cart', []))
    return render_template('index.html', featured=PRODUCTS[:2], cart_count=cart_count)

@app.route('/products')
def products():
    cart_count = len(session.get('cart', []))
    return render_template('products.html', products=PRODUCTS, cart_count=cart_count)

@app.route('/about')
def about():
    cart_count = len(session.get('cart', []))
    return render_template('about.html', cart_count=cart_count)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    cart_count = len(session.get('cart', []))
    if request.method == 'POST':
        flash('Thank you for reaching out! We have received your message.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', cart_count=cart_count)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    cart_count = len(session.get('cart', []))
    matched_candle = None
    if request.method == 'POST':
        vibe = request.form.get('vibe')
        if vibe == 'moody':
            matched_candle = PRODUCTS[0]
        elif vibe == 'warm':
            matched_candle = PRODUCTS[1]
        else:
            matched_candle = PRODUCTS[2]
            
    return render_template('quiz.html', matched_candle=matched_candle, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    # Find product by id
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        session['cart'].append(product)
        flash(f"Added {product['name']} to your bag.", "success")
        
    return redirect(request.referrer or url_for('products'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_count = len(session.get('cart', []))
    if 'cart' not in session or not session['cart']:
        # Default fallback item if cart is empty so checkout looks good
        cart_items = [PRODUCTS[0]]
    else:
        cart_items = session['cart']
        
    total_price = sum(item['price'] for item in cart_items)

    if request.method == 'POST':
        # Clear cart upon successful order
        session.pop('cart', None)
        return redirect(url_for('thank_you'))

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price, cart_count=cart_count)

@app.route('/thank-you')
def thank_you():
    cart_count = 0
    return render_template('thank_you.html', cart_count=cart_count)

if __name__ == '__main__':
    app.run(debug=True)