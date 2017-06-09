import RPi.GPIO as GPIO
import time
from random import randint

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi

PORT_NUMBER = 8000

GPIO.setmode(GPIO.BOARD)
RANGE = [[0,180],[50,120],[50,120],[50,120],[50,120]]
frequency_hertz = 50
pins = [8, 10, 12, 16, 18]
pwms = []
for i in range(0, len(pins)):
    GPIO.setup(pins[i], GPIO.OUT)
    pwms = pwms + [GPIO.PWM(pins[i], frequency_hertz)]

def degree2frequency(degree):
    frequency_hertz = 50
    ms_per_cycle = 1000 / frequency_hertz
    left_position = 0.40
    right_position = 2.5
    max_position = right_position - left_position
    position = degree * max_position / 180 + left_position;
    duty_cycle_percentage = position * 100 / ms_per_cycle
    return duty_cycle_percentage

def control(pwm, degree):
    duty = degree2frequency(degree)
    pwm.start(duty)

def reset(pwm):
    duty = degree2frequency(0)
    pwm.start(duty)

def generateCmd():
    ipwm = randint(0, 9) % 3
    d = randint(0, 180) % 180
    control(pwms[ipwm], d)

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
            servoid = int(float(parts[len(parts) - 2]))
            degree = int(float(parts[len(parts) - 1]))
            print(servoid, ' ', degree)
            control(pwms[servoid], degree)


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


for i in range(0,len(pwms)):
    pwms[i].stop()