Restaurant
==========

This project sets up a restaurant website using a database. The repository contains the restaurantDBsetup.py that sets up the database, the lotsOfMenus.py that populates my database with restaurants and menus, and project.py which creates a web server on port 5000. Project.py also utilizes CSS style sheets, JSON returns and utilizes the Google+ API for login as well as demonstrates CRUD operators for all items.

Technology
----------
-Python 2.7.10
-SQLite	
Special modules:
	-SQLAlchemy
	-BaseHTTPServer
	-FLask
	-WTForms
-Oracle VM VirtualBox 5.0.4
-Vagrant 1.7.4
-Google+ OAuth2 API
-Facebook OAuth2 API

Files
-----
/flask-wft
/static
	/black_user.gif
	/styles.css
	/top-banner.jpg
/templates
	/header.html
	/login.html
	/main.html
	/menu.html
	/menuItemDelete.html
	/menuItemEdit.html
	/menuItemNew.html
	/publicmenu.html
	/publicrestaurants.html
	/restaurantDelete.html
	/restaurantEdit.html
	/restaurantNew.html
	/restaurants.html
/ReadMe.md
/fb_client_secrets.json
/g_client_secrets.json
-lotsOfMenusUserDB.py
-project.py
-forms.py
-restaurantDBSetup.py

To Begin
--------
-Follow the instructions found here to install VirtualBox and Vagrant. https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true
-Install Oracle VM VirtualBox 5.0.4
-Install Vagrant 1.7.4
-Clone git repository from https://github.com/robertkohl125/Restaurant.git
-Navigate to fullstack/vagrant/PuppyShelter
--Files in this repository are listed above.
-From a command line run restaurantDBSetup.py the set up the database using
$ python restaurantDBSetup.py
-Then run lotsOfMenus.py to add restaurants and menus to the database using 
$ python lotsOfMenus.py
-Then run project.py using
$ python project.py

Contribute
----------
-Source Code: github.com/robertkohl125/Restaurant.git

Support
-------
If you are having issues, please let me know at: Robertkohl125@gmail.com
