Restaurant
==========

This project sets up a restaurant website using a database. The repository contains the restaurantDBsetup.py that sets up the database, the lotsOfMenus.py that populates my database with restaurants and menus, and two programs that create a web server. webserver.py demonstrates some basic HTML GET and POST functions on port 8080, and project.py creates a more well developed web server on port 5000. project.py also utilizes CSS style sheets, JSON returns and utilizes the Google+ API for login.

Technology
----------
-Python 2.7.10
-SQLite	
Special modules:
	-SQLAlchemy
	-BaseHTTPServer
	-FLask
-Oracle VM VirtualBox 5.0.4
-Vagrant 1.7.4

Files
-----
-ReadMe.md
-client_secrets.json
-lotsOfMenus.py
-project.py
-restaurantCRUD.py
-restaurantDBSetup.py
-webserver.py
-templates/login.html
-templates/menu.html
-templates/menuDelete.html
-templates/menuEdit.html
-templates/menuNew.html
-templates/restaurants.html
-templates/restaurantDelete.html
-templates/restaurantEdit.html
-templates/restaurantNew.html
-templates/restaurant.html
-static/styles.css

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
-Then run webserver.py or project.py.
$ python webserver.py
	-or- 
$ python project.py

Contribute
----------
-Source Code: github.com/robertkohl125/Restaurant.git

Support
-------
If you are having issues, please let me know at: Robertkohl125@gmail.com
