from flask import render_template, request, redirect, url_for, abort, session
from server import app, system
from datetime import datetime
from src.ingredient import Ingredient
import sys
'''
Website Structure:
- Home page '/'
- #Customer '/customer'
    - Menu pages '/customer/menu' 
        - Mains '/customer/mains'
            - Creation '/customer/mains/creation'
        - Sides '/customer/sides'
        - Drinks '/customer/drinks'
        - Sundaes '/customer/sundaes'
    - Review order '/customer/review/<order_id>'
    - Order tracking  '/customer/order/<order_id>'
- #Staff '/staff'
    - Login '/staff/login'
    - Logout '/staff/logout'
    - Order '/staff/order'
    - Inventory '/staff/inventory'
'''


'''
page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404


@app.route('/', methods=["GET", "POST"])
def home_page():
    print(session)
    if request.method == 'POST': 
        if request.form["button"] == "make_new_order":
            order_id = system.make_order()
            session['order_ID'] = order_id
            return redirect('/customer/menu/Mains')
        elif request.form["button"] == "continue_order":
            return redirect('/customer/menu/Mains')
        elif request.form["button"] == "search_order":
            return redirect(url_for('search_order', order_id=request.form['order_id']))
        elif request.form["button"] == "staff":
            return redirect(url_for('staff_homepage'))

    return render_template('home_page.html', system=system)


'''
Customer pages:
'''

def check_order_in_session():
    # check whether order_id in the session
    if 'order_ID' not in session:
        return render_template("error.html", error="Sorry, you need to create a new order first.")
    # check whether the order_id is in the system
    if not system.get_order(session['order_ID']):
        return render_template("error.html", error="Sorry, your order ID is no longer valid.")


@app.route('/customer/menu/<menu_name>', methods=["GET", "POST"])
def display_menu(menu_name):
    check_order_in_session()
    
    if request.method == 'POST':
        if "add_btn" in request.form.keys():
            item = system.get_item(request.form["add_btn"])
            if menu_name == "Mains":
                 system.add_default_main(session['order_ID'], item)
            else:
                system.add_items_in_orders(session['order_ID'], item)
        elif "mod_btn" in request.form.keys():
            item = system.get_item(request.form["mod_btn"])
            return redirect(url_for("modify_mains", item_name=item.name))
    
    menu = system.get_menu(menu_name)
    if not menu:
        print(f"not found {menu_name}")
        return redirect(url_for('page_not_found'))

    return render_template('customer_menus.html', menu_name=menu_name, menu=menu.display(), inventory=system.inventory)
    

@app.route('/customer/creation/<item_name>', methods=["GET", "POST"])
def modify_mains(item_name):
    check_order_in_session()
    
    item = system.get_item(item_name)
    print(item)
    print(system.inventory.display_unavailable_ingredients())
    if request.method == 'POST':
        if request.form['button'] == 'submit':
            for name, amount in request.form.items():
                if name == 'button':
                    continue
                if amount:
                    price = system.inventory.get_ingredient(name)._additional_price
                    ingredient = Ingredient(name,int(amount),additional_price=price)
                    if 'Bun' in name:       item.modify_buns(system.inventory,ingredient)
                    elif 'Wrap' in name:    item.modify_wraps(system.inventory,ingredient)
                    elif 'Patty' in name:   item.modify_patties(system.inventory,ingredient)
                    else:                   item.modify_other_ingredients(system.inventory,ingredient)
                if item._errors:
                    return render_template("customer_mains_creation.html", item=item, inventory=system.inventory, error=item._errors)
            system.add_items_in_orders(session['order_ID'], item)
            return redirect(url_for('review_order'))
    
    return render_template("customer_mains_creation.html", item=item, inventory=system.inventory, error=item._errors)


@app.route('/customer/review', methods=["GET", "POST"])
def review_order():
    check_order_in_session()

    order = system.get_order(session['order_ID'])
    if request.method == 'POST':
        if request.form["button"] == "checkout":
            order_id = session['order_ID']
            error = system.checkout(order_id)
            if error:
                return render_template("error.html", error=error)
            session.pop('order_ID')
            return render_template("customer_order_result.html", order_id=order_id)
        else:
            system.del_items_in_orders(order.order_id, request.form["button"])
    
    return render_template('customer_review_order.html', order=order)


@app.route('/customer/order/<order_id>')
def search_order(order_id):
    return render_template('customer_search_order_result.html', order=system.get_order(int(order_id)))


'''
Staff pages:
'''
@app.route('/staff')
def staff_homepage():
    if system.is_authenticated:
        return redirect(url_for('staff_order'))
    else:
        return redirect(url_for('staff_login'))


@app.route('/staff/login', methods=["GET", "POST"])
def staff_login():

    if request.method == 'POST':
        if request.form['button'] == "login":
            if system.staff_login(request.form['username'], request.form['password']):
                return redirect(url_for('staff_order'))
            else:
                return render_template('staff_login.html', username=request.form['username'], error=True)
        
        elif request.form['button'] == "cancel":
            return redirect(url_for('home_page')) 
    
    return render_template('staff_login.html', username=None, error=None)


@app.route('/staff/logout')
def staff_logout():
    system.staff_logout()
    return redirect(url_for('home_page'))


@app.route('/staff/order', methods=["GET", "POST"])
def staff_order():
    if not system.is_authenticated:
        return redirect(url_for('staff_login')) 

    if request.method == 'POST':
        order_id = int(request.form['button'])
        system.update_order(order_id)
        system.save_state() 

    return render_template('staff_order.html', system=system)


@app.route('/staff/inventory', methods=["GET", "POST"])
def staff_inventory():
    if not system.is_authenticated:
        return redirect(url_for('staff_login'))
    
    if request.method == 'POST':
        for name, amount in request.form.items():
            if amount:
                system.inventory.update_stock(name, float(amount))
        system.save_state()
    
    return render_template('staff_inventory.html', system=system)