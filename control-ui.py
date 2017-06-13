import serial
import time
from random import randint

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi

PORT_NUMBER=8000
USBCOM = 'COM4'
ser = serial.Serial(USBCOM)

def control(cmd):
    ser.write(cmd)

# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        if self.path.endswith(".html") or self.path.endswith(".jpg") or self.path.endswith(".gif") or self.path.endswith(".js") or self.path.endswith(".css")  or self.path.endswith(".map"):
            try:
                # Check the file extension required and
                # set the right mime type
                sendReply = False
                if self.path.endswith(".html"):
                    mimetype = 'text/html'
                    sendReply = True
                if self.path.endswith(".jpg"):
                    mimetype = 'image/jpg'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype = 'image/gif'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype = 'application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype = 'text/css'
                    sendReply = True

                if sendReply == True:
                    # Open the static file requested and send it
                    f = open(curdir + sep + self.path)
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(f.read())
                    f.close()
                return
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)
        else:
            parts = self.path.split('/')
            print(parts)
            servoid = parts[len(parts)-2]
            op = parts[len(parts) - 1]
            print(servoid, op)
            control(servoid+op+'\n')
            self.send_response(200)


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
