from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

HTML_BR = '</br>'

class ScopedDBSession():

    def __init__(self, engine):
        self.engine = engine

    def __enter__(self):
        self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        return self.session
    
    def __exit__(self, *args):
        self.session.remove()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    with ScopedDBSession(engine) as session:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurant_menu_item_json(restaurant_id, menu_id):
    with ScopedDBSession(engine) as session:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()
        return jsonify(MenuItems=[items.serialize])

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
    with ScopedDBSession(engine) as session:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    with ScopedDBSession(engine) as session:
        if request.method == 'POST':
            new_item = MenuItem(name = request.form['name'],
                price = request.form['price'],
                description = request.form['description'],
                restaurant_id = restaurant_id)
            session.add(new_item)
            session.commit()
            flash('new menu item created!')
            return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
        else:
            return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menuitem/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    with ScopedDBSession(engine) as session:
        edit_item = session.query(MenuItem).filter_by(id=menu_id).one()

        if request.method == 'POST':
            edit_item.name = request.form['name']
            edit_item.price = request.form['price']
            edit_item.description = request.form['description']
            session.add(edit_item)
            session.commit()
            flash('edit menu item saved!')
            return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
        else:
            return render_template('editmenuitem.html', restaurant_id = restaurant_id, 
                menu_id = menu_id, edit_item = edit_item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/menuitem/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    with ScopedDBSession(engine) as session:
        delete_item = session.query(MenuItem).filter_by(id=menu_id).one()

        if request.method == 'POST':
            session.delete(delete_item)
            session.commit()
            flash('menu item deleted!')
            return redirect(url_for('restaurant_menu', restaurant_id = restaurant_id))
        else:
            return render_template('deletemenuitem.html', restaurant_id = restaurant_id, 
                menu_id = menu_id, delete_item = delete_item)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)