from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurantDBSetup import Base, Restaurant, MenuItem

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


#Create a state tokent to prevent request forgery.
#Store it in the session for later validation.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
    login_session['state'] = state
    return render_template('login.html', STATE = state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(
            json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID does not match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
    
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route("/gdisconnect")
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        return response

    
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
@app.route('/')
@app.route('/restaurants')
def restaurants():

    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)


#shows the form for creating a new restaurant
@app.route('/restaurants/restaurantnew', methods = ['GET','POST'])
def restaurantNew():
    if 'username' not in login_session:
        return redirect('/login')
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
    if 'username' not in login_session:
        return redirect('/login')
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
    if 'username' not in login_session:
        return redirect('/login')
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
    if 'username' not in login_session:
        return redirect('/login')
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
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, menu_id = menu_id)
    if request.method == 'POST':
        editItem = MenuItem(
            name = request.form['new_name'], 
            course = request.form['new_course'],
            description = request.form['new_description'],
            price = request.form['new_price'])
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
    if 'username' not in login_session:
        return redirect('/login')
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