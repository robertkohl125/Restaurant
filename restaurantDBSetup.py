import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	"""Connects to the Restaurant table
	"""
	__tablename__ = 'restaurant'
	
	restaurant_id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	

class MenuItem(Base):
	"""Connects to the Restaurant table
	"""
	__tablename__ = 'menu_item'
	
	menu_id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
	restaurant = relationship(Restaurant)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine) 