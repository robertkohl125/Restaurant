#Restaurant
========================

This project sets up a restaurant website using a relational database. Project.py also utilizes CSS style sheets, JSON returns and utilizes the Google+ API and Facebook API for OAuth login as well as demonstrates CRUD operators for all items. Please view my commits for latest updates.

###Technology Used
----------
* Python 2.7.10
* Bootstrap
* SQLAlchemy
* SQLite
* Flask  
* Special modules:
    * SQLAlchemy
    * BaseHTTPServer
    * FLask
    * WTForms
* Oracle VM VirtualBox 5.0.4
* Vagrant 1.7.4
* Google+ OAuth2 API
* Facebook OAuth2 API

###Directory Structure
----------------------
```
+--README.md
+--fb_client_secrets.json
+--g_client_secrets.json
+--lotsOfMenusUserDB.py
+--project.py
+--forms.py
|   +--(Various Flask directories)
+--restaurantDBSetup.py
+--flask-wft
+--static
|   +--black_user.gif
|   +--styles.css
|   +--top-banner.jpg
+--templates
    +--header.html
    +--login.html
    +--main.html
    +--menu.html
    +--menuItemDelete.html
    +--menuItemEdit.html
    +--menuItemNew.html
    +--publicmenu.html
    +--publicrestaurants.html
    +--restaurantDelete.html
    +--restaurantEdit.html
    +--restaurantNew.html
    +--restaurants.html


```
###To Begin
-----------
1. Follow the instructions found [here][1] to install **VirtualBox** and **Vagrant**. 
1. Clone the Github repository [here][4].
1. Create Google+ and Facebook client secrets for OAuth and replace the following files:
    *fb_client_secrets.json
    *g_client_secrets.json
1. Navigate to **fullstack/vagrant/RMP** using the command shell. The directory structure is listed above.
1. From a command line run **restaurantDBSetup.py** the set up the database with the following command:
    * $ `python restaurantDBSetup.py`
1. Hit **ctrl**+**c** to stop the process.
1. Run **lotsOfMenus.py** to add restaurants and menus to the database with the following command: 
    * $ `python lotsOfMenus.py`
1. Run project.py again with the following command:
    * $ `python project.py`

###Support/Contact
----------
If you are having issues, please let me know. Contributions, tips and comments are welcome!
* Email: robertkohl125@gmail.com
* [Github Profile][5]
* [StackOverflow Profile][6]
* [LinkedIn Profile][7]

###License
----------
The MIT License (MIT)

Copyright (c) [2015] [Robert Kohl]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


[1]: https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true "Google Doc"
[2]: https://twilio-python.readthedocs.org/en/latest/ "twilio"
[3]: https://pythonhosted.org/Flask-Mail/ "Flask-Mail"
[4]: https://github.com/robertkohl125/Restaurant.git "Github repository"
[5]: https://github.com/robertkohl125 "Github Profile"
[6]: http://stackoverflow.com/users/2180707/robertkohl125?tab=profile "Stack Overflow Profile"
[7]: https://www.linkedin.com/in/robertkohl125 "LinkedIn"