# Objective 1

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

def get_db_session(dbstring):
    # Re-create the database
    engine = create_engine(dbstring)

    # Relate Tables to DB
    Base.metadata.bind = engine

    # SQL Session Wrapper
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

session = get_db_session('sqlite:///restaurantmenu.db')


class WebServerHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                restaurants = session.query(Restaurant).all()
                for r in restaurants:
                    output += "<div><h1>"+r.name+"</h1>"
                    
                        
                        
                    output += "</div>"
                # for each restaurant in the db
                # create an h1 tag for the name
                # create a ul li for the rest of its info
                # create a <br> for the nxt item
                output += "</body></html>"
                self.wfile.write(output)
                print (output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
	    pass
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print ("Web Server running on port %s" % port)

        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()


