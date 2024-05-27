from flask import Flask, render_template, request, session, redirect
from model import *
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database initialization
initialize_db(app)

# Routes
@app.route('/')
def index():
    products_with_sections = db.session.query(Product, Section).join(Section).all()
    return render_template('index.html', title='Home', products_with_sections=products_with_sections)


@app.route('/admin')
def admin_panel():
    if 'username' in session and session['role'] == 'admin':
        sections = Section.query.all() 
        products = Product.query.all()  # Fetch all sections/categories
        return render_template('admin_panel.html', title='Admin Panel', sections=sections, products = products)
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            session['username'] = user.username
            session['role'] = user.role
            return redirect('/admin' if user.role == 'admin' else '/')
        
    return render_template('login.html', title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        # Check if the username is already taken
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already taken."
        
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return "Registration successful!"
    
    return render_template('register.html', title='Register')

@app.route('/admin/add_section', methods=['GET', 'POST'])
def add_section():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        # image = request.form['image']
        
        new_section = Section(name=name, type=type)
        db.session.add(new_section)
        db.session.commit()
        return redirect('/admin')

    return render_template('add_section.html', title='Add Section')


@app.route('/admin/edit_section/<int:section_id>', methods=['GET', 'POST'])
def edit_section(section_id):
    section = Section.query.get(section_id)
    
    if request.method == 'POST':
        section.name = request.form['name']
        section.type = request.form['type']
        # section.image = request.form['image']
        db.session.commit()
        return redirect('/admin')  # Redirect to the admin panel after editing

    return render_template('edit_section.html', title='Edit Section', section=section)



@app.route('/admin/delete_section/<int:section_id>', methods=['GET', 'POST'])
def delete_section(section_id):
    section = Section.query.get(section_id)
    
    if request.method == 'POST':
        db.session.delete(section)
        db.session.commit()
        return redirect('/admin')

    return render_template('delete_section.html', title='Delete Section', section=section)

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    sections = Section.query.all()

    if request.method == 'POST':
        name = request.form['name']
        stock = request.form['stock']
        manufacture_date_str = request.form['manufacture_date']
        expiry_date_str = request.form['expiry_date']
        rate_per_unit = float(request.form['rate_per_unit'])
        section_id = int(request.form['section'])

        # Parse the date strings into datetime objects
        manufacture_date = datetime.strptime(manufacture_date_str, '%Y-%m-%d')
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')

        new_product = Product(name=name,stock=stock, manufacture_date=manufacture_date, expiry_date=expiry_date, rate_per_unit=rate_per_unit, section_id=section_id)
        db.session.add(new_product)
        db.session.commit()
        return redirect('/admin')  # Redirect to the admin panel after adding

    return render_template('add_product.html', title='Add Product', sections=sections)


@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    sections = Section.query.all()

    if request.method == 'POST':
        product.name = request.form['name']
        product.stock = request.form['stock']
        product.manufacture_date = datetime.strptime(request.form['manufacture_date'], '%Y-%m-%d')
        product.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')
        product.rate_per_unit = float(request.form['rate_per_unit'])
        product.section_id = int(request.form['section'])

        db.session.commit()
        return redirect('/admin')  # Redirect to the admin panel after editing

    return render_template('edit_product.html', title='Edit Product', product=product, sections=sections)


@app.route('/admin/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        return redirect('/admin')

    return render_template('delete_product.html', title='Delete Product', product=product)


@app.route('/purchases/add', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        user = User.query.filter_by(username=session.get('username')).first()
        user_id =user.id  # Assuming you have 'user_id' in the session
        product_id = int(request.form['product'])
        quantity = float(request.form['quantity'])
        product = Product.query.get(product_id)
        if (product.stock<quantity):
            return ('out of stock')
        new_purchase = Purchase(user_id=user_id, quantity=quantity, product_id=product_id, purchase_date=datetime.now())
        # new_purchase = Purchase(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_purchase)
        product.stock=product.stock-quantity
        db.session.commit()
        
        return redirect('/purchases')

    products = Product.query.all()
    return render_template('add_purchase.html', title='Add Purchase', products=products)

@app.route('/purchases', methods=['GET'])
def list_purchases():
    purchases = Purchase.query.join(Product).with_entities(Purchase, Product).all()

    return render_template('purchases.html', title='Purchases', purchases=purchases)




@app.route('/purchases/edit/<int:purchase_id>', methods=['GET', 'POST'])
def edit_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)
    users = User.query.all()
    products = Product.query.all()

    if request.method == 'POST':
        purchase.user_id = int(request.form['user'])
        purchase.product_id = int(request.form['product'])
        purchase.quantity = float(request.form['quantity'])
        
        db.session.commit()
        return redirect('/purchases')

    return render_template('edit_purchase.html', title='Edit Purchase', purchase=purchase, users=users, products=products)

@app.route('/purchases/delete/<int:purchase_id>', methods=['GET', 'POST'])
def delete_purchase(purchase_id):
    purchase = Purchase.query.get(purchase_id)

    if request.method == 'POST':
        db.session.delete(purchase)
        db.session.commit()
        return redirect('/purchases')

    return render_template('delete_purchase.html', title='Delete Purchase', purchase=purchase)

@app.route('/search/sections', methods=['GET'])
def search_sections():
    search_term = request.args.get('q', '').strip()
    sections = Section.query.filter(Section.name.ilike(f'%{search_term}%')).all()
    
    return render_template('search_sections.html', title='Search Sections', search_term=search_term, sections=sections)

@app.route('/search/products', methods=['GET'])
def search_products():
    search_term = request.args.get('q', '').strip()
    products = Product.query.filter(Product.name.ilike(f'%{search_term}%')).all()
    
    return render_template('search_products.html', title='Search Products', search_term=search_term, products=products)




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
