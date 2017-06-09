import SimpleHTTPServer
import SocketServer

PORT = 8000


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        else:
            parts = self.path.split('/')
            servoid = parts[len(parts) - 2]
            degree = parts[len(parts) - 1]
            print(servoid, ' ', degree)


Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
httpd.serve_forever()