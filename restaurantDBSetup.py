import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


#
class User(Base):
    """Connects to the User table
    """
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(250))
    picture = Column(String(250))


#
class Restaurant(Base):
    """Connects to the Restaurant table
    """
    __tablename__ = 'restaurant'
    
    restaurant_id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)


#
class MenuItem(Base):
    """Connects to the MenuItem table
    """
    __tablename__ = 'menu_item'
    
    menu_id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.restaurant_id'))
    restaurant = relationship(Restaurant)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Returns object data in easily serializable format
        return {
            'menu_id':self.menu_id,
            'name':self.name,
            'course':self.course,
            'description':self.description,
            'price':self.price,
            'restaurant_id':self.restaurant_id,
            'user_id':self.user_id,
        }



engine = create_engine('sqlite:///restaurant-menuitem-user.db')
Base.metadata.create_all(engine) 