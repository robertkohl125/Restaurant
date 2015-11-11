from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurantDBSetup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


#Making an API Endpoint for a restaurant menu(GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


#Making an API Endpoint for a menu item (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	item = session.query(MenuItem).filter_by(menu_id = menu_id).one()
	return jsonify(MenuItems=item.serialize)


#shows all of the restaurants
@app.route('/restaurants/')
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)


#shows the form for creating a new restaurant
@app.route('/restaurants/restaurantnew', methods = ['GET','POST'])
def restaurantNew():
	restaurant = session.query(Restaurant)
	if request.method == 'POST':
		newRestaurantName = Restaurant(name = request.form['new_name'])
		session.add(newRestaurantName)
		session.commit
		flash("New restaurant created!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('restaurantNew.html', restaurant = restaurant)


#shows the form for editing the name of a restaurant
@app.route('/restaurants/<int:restaurant_id>/restaurantedit', methods = ['GET','POST'])
def restaurantEdit(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		editRestaurantName = MenuItem(name = request.form['new_name'])
		for r in restaurant:
			r.name = editRestaurantName.name
		session.add(r)
		session.commit
		flash("A restaurant has been edited!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('restaurantEdit.html', restaurant = restaurant)


#shows the form for deleting a restaurant
@app.route('/restaurants/<int:restaurant_id>/restaurantdelete', methods = ['GET','POST'])
def restaurantDelete(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		for r in restaurant:
			deleteRestaurant = Restaurant(restaurant_id = restaurant_id)
		session.delete(r)
		session.commit
		flash("A restaurant has been deleted!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('restaurantDelete.html', restaurant = restaurant)


#Methods for Menus
#shows the menu for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/') #decorator function allowing the website to be found at "/hello" also
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id).all()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).order_by(MenuItem.course)
	return render_template('menu.html', restaurant = restaurant, items = items)


#shows the form for creating a new menu item for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/menuitemnew/', methods = ['GET','POST'])
def menuItemNew(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id=restaurant_id)
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], 
			course = request.form['course'],
			description = request.form['description'],
			price = request.form['price'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit
		flash("A menu item has been created!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('menuItemNew.html', restaurant = restaurant)


#shows the form for editing menu items for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/menuItemEdit', methods = ['GET','POST'])
def menuItemEdit(restaurant_id, menu_id):
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
		flash("A menu item has been edited!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('menuItemEdit.html', restaurant = restaurant, items = items)


#shows the form for deleting menu items for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/menuItemDelete/', methods = ['GET','POST'])
def menuItemDelete(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, menu_id = menu_id)
	if request.method == 'POST':
		for i in items:
			deleteItem = MenuItem(menu_id = menu_id)
		session.delete(i)
		session.commit
		flash("A menu item has been deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('menuItemDelete.html', restaurant = restaurant, items = items)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000) #listen on all public IP addresses for port 5000