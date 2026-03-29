from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# قاعدة البيانات
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/mavi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# النماذج
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, default="")
    image = db.Column(db.String(200), default="")
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False)
    items_json = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="new")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# الروابط الأساسية
@app.route('/menu/<int:table>')
def menu(table):
    session['table'] = table
    categories = Category.query.all()
    return render_template('menu.html', categories=categories, table=table)

@app.route('/category/<int:cat_id>')
def category(cat_id):
    category = Category.query.get_or_404(cat_id)
    items = Item.query.filter_by(category_id=cat_id).all()
    table = session.get('table', 1)
    return render_template('category.html', category=category, items=items, table=table)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == int(data['id']):
            item['quantity'] = item.get('quantity', 1) + 1
            session['cart'] = cart
            return jsonify({"status": "success", "cart_count": len(cart)})
    cart.append({
        'id': int(data['id']),
        'name': data['name'],
        'price': float(data['price']),
        'quantity': 1
    })
    session['cart'] = cart
    return jsonify({"status": "success", "cart_count": len(cart)})

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item.get('quantity', 1) for item in cart_items)
    table = session.get('table', 1)
    return render_template('cart.html', cart=cart_items, total=total, table=table)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    cart = session.get('cart', [])
    if not cart:
        return jsonify({"error": "السلة فارغة"}), 400
    total = sum(item['price'] * item.get('quantity', 1) for item in cart)
    items_json = json.dumps(cart)
    order = Order(table_number=session.get('table'), items_json=items_json, total=total)
    db.session.add(order)
    db.session.commit()
    session.pop('cart', None)
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/admin')
def admin_dashboard():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/dashboard.html', orders=orders)

# تشغيل التطبيق
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)