from flask import Flask
from sqlalchemy import create_engine, Integer
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

HTML_BREAK = "</br>"

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    output = ""
    if restaurant != []:
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

        for item in items:
            output += item.name + HTML_BREAK
            output += item.price + HTML_BREAK
            output += item.description +HTML_BREAK
            output += HTML_BREAK

    return output 

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)