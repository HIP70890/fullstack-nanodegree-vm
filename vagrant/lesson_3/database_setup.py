import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurant'

    name = Column(String(80), nullable = False) # Name of the restaurant
    id = Column(Integer, primary_key = True) # ID of the restaurant, as primary key

class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable = False) # Name of the menu item
    id = Column(Integer, primary_key = True) # ID of the menu item, as primary key
    course = Column(String(259)) # Type of menu item
    description = Column(String(250)) # Description
    price = Column(String(8)) # Price of the menu item
    restaurant_id = Column(Integer, ForeignKey('restaurant.id')) # Foreign key to the restaurant owning this menut item
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name'          : self.name,
            'description'   : self.description,
            'id'            : self.id,
            'price'         : self.price,
            'course'        : self.course,
        }

engine = create_engine('sqlite:///restaurantmenu.db')
session_factory = sessionmaker(bind=engine)
RestaurantDBSession = scoped_session(session_factory)
Base.metadata.create_all(engine)
