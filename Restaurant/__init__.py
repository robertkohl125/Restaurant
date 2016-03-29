from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurantDBSetup import Base, Restaurant, MenuItem, User
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from requests_oauthlib import OAuth2Session
import httplib2
import json
import requests
import forms
app = Flask(__name__)


engine = create_engine('postgresql://catalog:catalog@locathost/itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


#Create a state tokent to prevent request forgery.
#Store it in the session for later validation.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)


#Route for Google+ OAuth2 from login.html
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('g_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    CLIENT_ID = json.loads(open('g_client_secrets.json', 'r').read())['web']['client_id']
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
    
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    else:
        login_session['user_id'] = user_id

    output = ''
    output += '<h2>Welcome Google+ user '
    output += login_session['username']
    output += '!</h2>'
    output += '<h4><b>gplus_id:</b>'
    output += login_session['gplus_id']
    output += '<br>'
    output += '<b>credentials:</b>'
    output += login_session['credentials']
    output += '<br>'
    output += '<b>email:</b>'
    output += login_session['email']
    output += '<br>'
    output += '</h4>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
     150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


#Route for Google+ OAuth2 disconnect()
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
    if result['status'] != '200':
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        return response


#Route for Facebook OAuth2 from login.html
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    app_id = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']

    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id,app_secret,access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print 'facebook1 result:', result
    userinfo_url = "http://graph.facebook.com/v2.5/me"

    token = result.split("&")[0]
    print token

    url = 'https://graph.facebook.com/v2.5/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print 'facebook2 result:', result 
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    url = 'https://graph.facebook.com/v2.5/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print 'facebook3 result:', result
    data = json.loads(result)
    login_session['picture'] = data["data"]["url"]

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    else:
        login_session['user_id'] = user_id

    output = ''
    output += '<h2>Welcome Facebook user '
    output += login_session['username']
    output += '!</h2>'
    output += '<h4><b>facebook_id:</b>'
    output += login_session['facebook_id']
    output += '<br>'
    output += '<b>access_token:</b>'
    output += login_session['access_token']
    output += '<br>'
    output += '<b>email:</b>'
    output += login_session['email']
    output += '<br>'
    output += '</h4>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
     150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "Done!"
    return output


#Route for Facebook OAuth2 disconnect()
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "You have been logged out."



#Route for disconnect and routes to proper disconnect method()
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['user_id']
        del login_session['email']
        del login_session['picture']
        flash("You have been logged out.")
        return redirect(url_for('restaurants'))
    else:
        flash("You were not logged in to begin with!")
        return redirect(url_for('restaurants'))

    
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
    if 'username' not in login_session:
        return render_template('publicrestaurants.html', restaurants = restaurants)
    else:
        return render_template('restaurants.html', restaurants = restaurants)


#shows the form for creating a new restaurant
@app.route('/restaurants/restaurantnew', methods = ['GET','POST'])
def restaurantNew():
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant)
    form = forms.RestaurantForm(request.form)
    if request.method == 'POST' and form.validate():
        new_restaurant = {
                    'name': form.name.data, 
                    'address': form.address.data,
                    'city': form.city.data,
                    'state': form.state.data,
                    'zipCode': form.zipCode.data,
                    'website': form.website.data,
                    'image': form.image.data,
                    'user_id': login_session['user_id']}
        createRestaurant(new_restaurant)
        flash("New restaurant created!")
        return redirect(url_for('restaurants'))
    else:
        return render_template('restaurantNew.html', 
            restaurant = restaurant, 
            form = form)


#Method for creating a restaurant.
def createRestaurant(new_restaurant):
    newRestaurant = Restaurant(
        name = new_restaurant['name'],
        address = new_restaurant['address'],
        city = new_restaurant['city'],
        state = new_restaurant['state'],
        zipCode = new_restaurant['zipCode'],
        website = new_restaurant['website'],
        image = new_restaurant['image'],
        user_id = new_restaurant['user_id'])
    session.add(newRestaurant)
    session.commit()


#shows the form for editing the name of a restaurant
@app.route('/restaurants/<int:restaurant_id>/restaurantedit', methods = ['GET','POST'])
def restaurantEdit(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
    for r in restaurant:
        r
    if r.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"
    form = forms.RestaurantForm(request.form)
    if request.method == 'POST' and form.validate():
        edit_restaurant = {
                    'name': form.name.data, 
                    'address': form.address.data,
                    'city': form.city.data,
                    'state': form.state.data,
                    'zipCode': form.zipCode.data,
                    'website': form.website.data,
                    'image': form.image.data}
        editRestaurant(edit_restaurant, restaurant_id)
        flash("%s has been edited." % r.name)
        return redirect(url_for('restaurants'))
    else:
        return render_template('restaurantEdit.html', 
            restaurant = restaurant,
            form = form)


#Method for creating a restaurant.
def editRestaurant(edit_restaurant, restaurant_id):
    restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
    updateRestaurant = Restaurant(
        name = edit_restaurant['name'],
        address = edit_restaurant['address'],
        city = edit_restaurant['city'],
        state = edit_restaurant['state'],
        zipCode = edit_restaurant['zipCode'],
        website = edit_restaurant['website'],
        image = edit_restaurant['image'])
    for r in restaurant:
        r.name = updateRestaurant.name
        r.address = updateRestaurant.address
        r.city = updateRestaurant.city
        r.state = updateRestaurant.state
        r.zipCode = updateRestaurant.zipCode
        r.website = updateRestaurant.website
        r.image = updateRestaurant.image
    session.add(r)
    session.commit()


#shows the form for deleting a restaurant
@app.route('/restaurants/<int:restaurant_id>/restaurantdelete', methods = ['GET','POST'])
def restaurantDelete(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
    for r in restaurant:
        r
    if r.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        for r in restaurant:
            r = r
        session.delete(r)
        flash("%s has been deleted!" % r.name)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        return render_template('restaurantDelete.html', restaurant = restaurant)


#Methods for Menus
#shows the menu for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id).all()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).order_by(MenuItem.course)
    for r in restaurant:
        r.user_id
    creator = getUserInfo(r.user_id)
    if 'username' not in login_session or creator.user_id != login_session['user_id']:
        return render_template('publicmenu.html', 
            restaurant = restaurant, 
            items = items,
            creator = creator)
    else:
        return render_template('menu.html', 
            restaurant = restaurant, 
            items = items,
            creator = creator)



#shows the form for creating a new menu item for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/menuitemnew/', methods = ['GET','POST'])
def menuItemNew(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    user_id=login_session['user_id']
    restaurant = session.query(Restaurant).filter_by(restaurant_id=restaurant_id)
    form = forms.MenuItemForm(request.form)
    if request.method == 'POST' and form.validate():
        newItem = MenuItem(
            name = request.form['name'], 
            course = request.form['course'],
            description = request.form['description'],
            price = request.form['price'], 
            restaurant_id = restaurant_id, 
            user_id=user_id)
        session.add(newItem)
        session.commit()
        flash("A menu item has been created: %s" % newItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('menuItemNew.html', 
            restaurant = restaurant, 
            form = form)


#shows the form for editing menu items for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/menuItemEdit', methods = ['GET','POST'])
def menuItemEdit(restaurant_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
    for r in restaurant:
        r
    if r.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, menu_id = menu_id)
    form = forms.MenuItemForm(request.form)
    if request.method == 'POST' and form.validate():
        editItem = MenuItem(
            name = request.form['name'], 
            course = request.form['course'],
            description = request.form['description'],
            image = request.form['image'],
            price = request.form['price']
            )
        for i in items:
            i.name = editItem.name
            i.course = editItem.course
            i.description = editItem.description
            i.image = editItem.image
            i.price = editItem.price
        session.add(i)
        session.commit()
        flash("%s has been edited." % editItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('menuItemEdit.html', 
            restaurant = restaurant, 
            items = items,
            form = form)


#shows the form for deleting menu items for a selected restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/menuItemDelete/', methods = ['GET','POST'])
def menuItemDelete(restaurant_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, menu_id = menu_id)
    restaurant = session.query(Restaurant).filter_by(restaurant_id = restaurant_id)
    for r in restaurant:
        r
    if r.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this restaurant. Please create your own restaurant in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        for i in items:
            deleteItem = MenuItem(menu_id = menu_id)
        session.delete(i)
        session.commit()
        flash("A menu item has been deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('menuItemDelete.html', restaurant = restaurant, items = items)


#Method to get user id from email address.
def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        print user.user_id
        return user.user_id
    except:
        return None


#Method to get user info from user id.
def getUserInfo(user_id):
    user = session.query(User).filter_by(user_id = user_id).one()
    print 'getUserInfo():'
    print user.user_id
    print user.name
    print user.email
    print user.picture
    return user


#Creates a user from login_session data in User table
def createUser(login_session):
    print 'createUser():'
    print login_session['username']
    print login_session['email']
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    print "User %s created." % user.name
    getUserInfo()
    user_id=login_session['user_id']
    return user.user_id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8080) #listen on all public IP addresses for port 8080