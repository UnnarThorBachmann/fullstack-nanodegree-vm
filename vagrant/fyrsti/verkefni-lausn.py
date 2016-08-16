import cgi

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                restaurants = session.query(Restaurant).order_by(Restaurant.name.asc()).all()
                output = ""
                output += "<html><body>"
                output += '<h1><a href="/new">Create new restaurant</a></h1>'
                for restaurant in restaurants:
                    id_restaurant = restaurant.id
                    output += "<h1>%s</h1> <a href='/%s/edit'>edit</a> <a href='/%s/delete'>delete</a>"% (str(restaurant.name),id_restaurant,id_restaurant)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            elif self.path.endswith("/new"):
                 self.send_response(200)
                 self.send_header('Content-type', 'text/html')
                 self.end_headers()
                 
                 output = ""
                 output += "<html><body>"
                 output += "<h1>New restaurant</h1>" 
                 output += '<form method="POST" enctype="multipart/form-data" action="/new">'
                 output += '<input name="message" type="text">' 
                 output += '<input type="submit" value="Submit"> </form>' 
                 output += "</body></html>"
                 self.wfile.write(output)
                 return
            elif self.path.endswith("/edit"):
                 self.send_response(200)
                 self.send_header('Content-type', 'text/html')
                 self.end_headers()
                 url = self.path.split("/")[-2]
                 print "url",url,len(url)
                 restaurant = session.query(Restaurant).filter(Restaurant.id==url).first()
                 output = ""
                 output += "<html><body>"
                 output += "<h1> %s </h1>" % restaurant.name
                 output += '<form method="POST" enctype="multipart/form-data" action="/%s/edit>' % url
                 output += '<label>Name:</label><input name="message" type="text" value="%s">' % restaurant.name
                 output += '<input type="submit" value="Submit"> </form>' 
                 output += "</body></html>"
                 self.wfile.write(output)
                 return
            elif self.path.endswith("/delete"):
                 self.send_response(200)
                 self.send_header('Content-type', 'text/html')
                 self.end_headers()
                 url = self.path.split("/")[-2]
                 
                 
                 restaurant = session.query(Restaurant).filter(Restaurant.id == url).first()

                 output = ""
                 output += "<html><body>"
                 output += "<h1>Do you want to delete %s?</h1>" % restaurant.name
                 output += '<form method="POST" enctype="multipart/form-data" action="/%s/delete">' % url
                 output += '<input type="submit" value="Delete"> </form>'
                 output += "</body></html>"
                 self.wfile.write(output)
                 
                 return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                 id_selected = self.path.split("/")[-2]
                 self.send_response(301)
                 self.send_header('Content-type', 'text/html')

                 self.send_header('Location', '/restaurants')
                 self.end_headers()
                 ctype, pdict = cgi.parse_header(
                 self.headers.getheader('content-type'))
                 if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                 print "Alrei aftur", str(messagecontent)
                 
                 restaurant = session.query(Restaurant).filter(Restaurant.id == id_selected).first()
                 print restaurant.id
                 restaurant.name = messagecontent[0]
                 print messagecontent[0]
                 session.add(restaurant)
                 session.commit()
            elif self.path.endswith("/new"):
                 self.send_response(301)
                 self.send_header('Content-type', 'text/html')
                 self.send_header('Location', '/restaurants')
                 self.end_headers()
                 ctype, pdict = cgi.parse_header(
                 self.headers.getheader('content-type'))
                 if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                 
                 restaurant = Restaurant(name=messagecontent[0])
                 session.add(restaurant)
                 session.commit()
                 
            elif self.path.endswith("/delete"):
                 print "prump"
                 id_selected = self.path.split("/")[-2]
                 self.send_response(301)
                 self.send_header('Content-type', 'text/html')
                 self.send_header('Location', '/restaurants')
                 self.end_headers()
                 
                 ctype, pdict = cgi.parse_header(
                 self.headers.getheader('content-type'))
                 if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                 
                 restaurant = session.query(Restaurant).filter(Restaurant.id == id_selected).first()
                 print restaurant.name
                 session.delete(restaurant)
                 session.commit()
        except:
              pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
