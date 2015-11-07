from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurantDBSetup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


#Get and Post handler
class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			# Creates page listing all restaurants with an edit and delete link for each
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<h2>Restaurants</h2></br>"
				output += "<a href='/restaurants/new'> Add a restaurant here </a></br></br>"
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output += "<html><body>"
				for r in restaurants:
					output += r.name
					output += "</br>"
					output += "<a href='/restaurants/%s/edit'>Edit</a>" % r.restaurant_id
					output += "</br>"
					output += "<a href='/restaurants/%s/delete'>Delete</a>" % r.restaurant_id
					output += "</br></br></br>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			# Creates page to create a new restaurant
			if self.path.endswith("/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"				
				output += "<form method ='post' enctype ='multipart/form-data' actions='/new'>\
					New Restaurant Name: <input type='text' name='newRestaurantName' ><br>"
				output += "<input type='submit' value='Create'>"
				output += "</form>"
				output += "<p>Enter the name of the new restaurant here and click Create.</p>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			# Creates page to edit a restaurants name
			if self.path.endswith("/edit"):
				r_id_path = self.path.split("/")[2] # Returns with the third element of the URL array, which is the restaurant.name that is assigned in the /restaurant main
				restaurant = session.query(Restaurant).filter_by(restaurant_id = r_id_path).one()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"				
				output += "<form method ='POST' enctype ='multipart/form-data' actions='/edit'>\
					%s shall now be called: <input type='text' name='editRestaurantName' ><br>" % restaurant.name
				output += "<input type='submit' value='Submit Rename'>"
				output += "</form>"
				output += '<p>Enter the new name for %s here and click "Submit Rename".</p>' % restaurant.name
				output += "</body></html>"
				self.wfile.write(output)
				return

			# Creates page to delete a restaurant
			if self.path.endswith("/delete"):
				r_id_path = self.path.split("/")[2]
				restaurant = session.query(Restaurant).filter_by(restaurant_id = r_id_path).one()
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h3>You are about to delete %s from the database!!!</h3>" % restaurant.name			
				output += "<form method ='post' enctype ='multipart/form-data' actions='/delete'>\
					Cannot be undone! Please confirm:<input type='submit' value='Confirm'>"
				output += "</form>"
				output += "</body></html>"
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path) 

	def do_POST(self):
		try:
			if self.path.endswith("/new"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					entry = fields.get("newRestaurantName")

					newRestaurant = Restaurant(name=entry[0])
					session.add(newRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', "/restaurants")
					self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					entry = fields.get("editRestaurantName")
					rIDpath = self.path.split("/")[2]
					rQueryEdit = session.query(Restaurant).filter_by(restaurant_id = rIDpath).one()
					print rQueryEdit
					if rQueryEdit != []:
						rQueryEdit.name = entry[0]
					session.add(rQueryEdit)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', "/restaurants")
					self.end_headers()

			if self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					r_id_path = self.path.split("/")[2]
					rQueryDel = session.query(Restaurant).filter_by(\
						restaurant_id = r_id_path).one()
					print rQueryDel
					if rQueryDel:
						session.delete(rQueryDel)
						session.commit()
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', "/restaurants")
						self.end_headers()

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()
		print "Web server stopped"

if __name__ == '__main__':
	main()