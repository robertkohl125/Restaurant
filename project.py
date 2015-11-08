from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurantDBSetup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/restaurants/')
def restaurants():
	restaurants = session.query(Restaurant).all()
	output = ""
	output += "<h2>Restaurants</h2></br>"
	output += "<a href='/restaurants/new'> Add a restaurant here </a></br></br>"
	output += "<html><body>"
	for r in restaurants:
		output += r.name
		output += "</br>"
		output += "<a href='/restaurants/%s'>View</a>" % r.restaurant_id
		output += "</br>"
		output += "<a href='/restaurants/%s/edit'>Edit</a>" % r.restaurant_id
		output += "</br>"
		output += "<a href='/restaurants/%s/delete'>Delete</a>" % r.restaurant_id
		output += "</br></br></br>"
	output += "</body></html>"
	return output

@app.route('/restaurants/new/')
def newRestaurant():
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.restaurant_id)
	output = ''
	output += "<form method ='post' enctype ='multipart/form-data' actions='/new'>\
		New Restaurant Name: <input type='text' name='newRestaurantName' ><br>"
	output += "<input type='submit' value='Create'></br></br>"
	return output

@app.route('/restaurants/<int:restaurant_id>/') #decorator function allowing the website to be found at "/hello" also
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(restaurant_id=Restaurant.restaurant_id).first()
	items = session.query(MenuItem).filter_by(restaurant_id = Restaurant.restaurant_id)
	output = ''
	output += '<h2>'
	output += restaurant.name
	output += '</h2>' 
	output += "<a href='/restaurants/%s/menu/newitem'> Add a menu item here </a></br></br>"  % restaurant.restaurant_id
	for i in items:
		output += i.name
		output += " (<a href='/restaurants/%s/menu/%s/edit'>Edit</a> /" % (i.restaurant_id, i.menu_id)
		output += " "
		output += "<a href='/restaurants/%s/menu/%s/delete'>Delete</a>)" % (i.restaurant_id, i.menu_id)
		output += '</br>'
		output += i.price
		output += '</br>'
		output += i.description
		output += "</br>"

		output += "</br></br></br>"
	return output

@app.route('/restaurants/<int:restaurant_id>/menu/newitem/')
def newMenuItem(restaurant_id):
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.restaurant_id)
	output = ''
	output += '<h2>'
	output += restaurant.name
	output += '</h2>' 
	output += "<form method ='post' enctype ='multipart/form-data' actions='/new'>\
		New Menu Item Name: <input type='text' name='name' ><br>"
	output += "Course: <input type='text' name='course' ><br>"
	output += "Description: <input type='text' name='description' ><br>"
	output += "Price: <input type='text' name='price' ><br>"
	output += "<input type='submit' value='Create'>"
	return output


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.restaurant_id, menu_id = menu_id)
	output = ''
	output += '<h2>'
	output += restaurant.name
	output += '</h2>' 
	output += "<form method ='post' enctype ='multipart/form-data' actions='/new'><br>"
	for i in items:
		output += i.name
		output += "</br>New Name: <input type='text' name='name' ><br>"
		output += '</br>'
		output += i.price
		output += "</br>New Price: <input type='text' name='price' ><br>"
		output += '</br>'
		output += i.description
		output += "</br>New Description: <input type='text' name='description' ><br>"
		output += '</br>'
		output += '</br>'
	output += "<input type='submit' value='Edit'>"
	return output


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.restaurant_id, menu_id = menu_id)
	output = ''
	output += '<h2>'
	output += restaurant.name
	output += '</h2>' 
	for i in items:
		output += i.name
		output += '</br>'
		output += i.price
		output += '</br>'
		output += i.description
		output += '</br>'
		output += '</br>'
	output += 'This action CANNOT be undone. Please confirm and press "Delete"'
	output += '</br>'
	output += "<input type='submit' value='Delete'>"
	return output


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000) #listen on all public IP addresses for port 5000