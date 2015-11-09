from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurantDBSetup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


#shows all of the restaurants
@app.route('/restaurants/')
def restaurants():
	restaurants = session.query(Restaurant).all()
	output = ""
	output += "<h1>Restaurants:</h1></br>"
	output += "<h3><a href='/restaurants/newrestaurant'> To add a restaurant, click here. </a></br></br></h3>"
	output += "</br>"
	output += "<html><body>"
	for r in restaurants:
		output += "<h3>"
		output += r.name
		output += "</h3>"
		output += "<a href='/restaurants/%s'>View Menu</a>" % r.restaurant_id
		output += " "
		output += "<a href='/restaurants/%s/editrestaurant'>Edit</a>" % r.restaurant_id
		output += " "
		output += "<a href='/restaurants/%s/deleterestaurant'>Delete</a>" % r.restaurant_id
		output += "</br></br></br>"
	output += "</body></html>"
	return output


#shows the form for creating a new restaurant
@app.route('/restaurants/newrestaurant', methods = ['GET','POST'])
def newRestaurant():
	restaurant = session.query(Restaurant)
	if request.method == 'POST':
		newRestaurantName = Restaurant(name = request.form['new_name'])
#		r = Restaurant(newRestaurantName)
		session.add(newRestaurantName)
		session.commit
		return redirect(url_for('restaurants'))
	else:
		return render_template('newRestaurant.html', restaurant = restaurant)


#shows the form for editing the name of a restaurant
@app.route('/restaurants/<int:restaurant_id>/editrestaurant', methods = ['GET','POST'])
def editRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		editRestaurantName = MenuItem(name = request.form['new_name'])
		for r in restaurant:
			r.name = editRestaurantName.name
		session.add(r)
		session.commit
		return redirect(url_for('restaurants'))
	else:
		return render_template('editRestaurant.html', restaurant = restaurant)


#shows the form for deleting a restaurant
@app.route('/restaurants/<int:restaurant_id>/deleterestaurant', methods = ['GET','POST'])
def deleteRestaurant(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		for r in restaurant:
			deleteRestaurant = Restaurant(restaurant_id = restaurant_id)
		session.delete(r)
		session.commit
		return redirect(url_for('restaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant = restaurant)


#Methods for Menus
#shows the menu for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/') #decorator function allowing the website to be found at "/hello" also
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id).all()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).order_by(MenuItem.course)
	return render_template('menu.html', restaurant = restaurant, items = items)


#shows the form for creating a new menu item for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/newitem/', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id=restaurant_id)
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], 
			course = request.form['course'],
			description = request.form['description'],
			price = request.form['price'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant = restaurant)


#shows the form for editing menu items for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edititem', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, menu_id = menu_id)
	if request.method == 'POST':
		editItem = MenuItem(
			name = request.form['new_name'], 
			course = request.form['new_course'],
			description = request.form['new_description'],
			price = request.form['new_price'])
#			restaurant_id = restaurant_id)
		for i in items:
			i.name = editItem.name
			i.course = editItem.course
			i.description = editItem.description
			i.price = editItem.price
		session.add(i)
		session.commit
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('editMenuItem.html', restaurant = restaurant, items = items)


#shows the form for deleting menu items for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/deleteitem/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.restaurant_id, menu_id = menu_id)
	if request.method == 'POST':
		for i in items:
			deleteItem = MenuItem(menu_id = menu_id)
		session.delete(i)
		session.commit
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant = restaurant, items = items)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000) #listen on all public IP addresses for port 5000