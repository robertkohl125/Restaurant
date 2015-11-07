from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurantDBSetup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


'''To CREATE data in a DB
'''
def CREATE():
	myFirstRestaurant = Restaurant(name = "Pizza Palace")
	session.add(myFirstRestaurant)
	session.commit()
	session.query(Restaurant).all()
	cheesepizza = (MenuItem(
		name = "Cheese Pizza", 
		description = "Made with all natural ingredients and fresh mozzarella", 
		course = "Entree", 
		price = "$8.99", 
		restaurant = myFirstRestaurant))


'''To READ data from a DB
'''
def READ():
	firstResult = session.query(Restaurant).first()
	firstResult.name
	print firstResult.name
	# Prints the first result of a query of the Restaurant table
	items = session.query(Restaurant).all()
	for item in items:
	    print item.name
	# Prints all the menu items found querying the MenuItem table


'''To UPDATE data from a DB
'''
def UPDATE():
	veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
	# 1 Execute a query to find the row and store it in a variable 
	# in this case, the variable is "veggieBurgers"
	for veggieBurger in veggieBurgers:
		print veggieBurger.menu_id
		print veggieBurger.price
		print veggieBurger.restaurant.name
		print "\n" #extra carriage return to keep results tidy


	for veggieBurger in veggieBurgers:
		if veggieBurger.price != '$2.99':
			veggieBurger.price = '$2.00'
	# 2 Run an if statement to find all values in the variable
			session.add(veggieBurger)
	# 3 add the updated variable to the session (within the for statement)
		session.commit()
	# 4 commit the session


'''To DELETE from a DB
'''
def DELETE():
	spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').all()
	# 1 Execute a query to find the row and store it in a variable 
	# in this case, the variable is "spinach"
	print spinach.restaurant.name
	session.delete(spinach)
	# 2 Perform the delete
	session.commit()
	# 3 commit the session

#CREATE()
READ()
#UPDATE()
#DELETE()
