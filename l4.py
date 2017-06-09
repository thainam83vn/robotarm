import RPi.GPIO as GPIO
import time
from random import randint

GPIO.setmode(GPIO.BOARD)
RANGE = [[0,180],[50,120],[50,120],[50,120],[50,120]]
frequency_hertz = 50
pins = [8, 10, 12, 16, 18]
pwms = []
for i in range(0, len(pins)):
    GPIO.setup(pins[i], GPIO.OUT)
    pwms = pwms + [GPIO.PWM(pins[i], frequency_hertz)]


#pwm = GPIO.PWM(pin_number, frequency_hertz)
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

for i in range(0,len(pwms)):
    reset(pwms[i])
    time.sleep(.5)

for i in range(100):
    generateCmd()
    time.sleep(.5)
    control(pwms[4], 0)
    time.sleep(.5)
    control(pwms[4], 90)
    time.sleep(.5)
    control(pwms[4], 180)
    time.sleep(.5)


for i in range(0,len(pwms)):
    reset(pwms[i])
    time.sleep(.5)

for i in range(0,len(pwms)):
    pwms[i].stop()


GPIO.cleanup()

