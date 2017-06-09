import RPi.GPIO as GPIO
import time

def degree2frequency(degree):
    frequency_hertz = 50
    ms_per_cycle = 1000 / frequency_hertz
    left_position = 0.40
    right_position = 2.5
    max_position = right_position - left_position
    position = degree * max_position / 180 + left_position;
    duty_cycle_percentage = position * 100 / ms_per_cycle
    return duty_cycle_percentage


GPIO.setmode(GPIO.BOARD)

pin_number = 8

GPIO.setup(pin_number, GPIO.OUT)

frequency_hertz = 50
pwm = GPIO.PWM(pin_number, frequency_hertz)

left_position = 0.40
right_position = 2.5
middle_position = (right_position - left_position) / 2 + left_position

positionList = [left_position, middle_position, right_position, middle_position]

ms_per_cycle = 1000 / frequency_hertz

for i in range(3):
    # This sequence contains positions from left to right
    # and then back again.  Move the motor to each position in order.
    # for position in positionList:
    #     duty_cycle_percentage = position * 100 / ms_per_cycle
    #     print("Position: " + str(position))
    #     print("Duty Cycle: " + str(duty_cycle_percentage))
    #     print("")
    #     pwm.start(duty_cycle_percentage)
    #     time.sleep(.5)

    for x in range(0, 180, 10):
        duty_cycle_percentage = degree2frequency(x)
        print("Position: " + str(x))
        print("Duty Cycle: " + str(duty_cycle_percentage))
        print("")
        pwm.start(duty_cycle_percentage)
        time.sleep(.2)

pwm.stop()

GPIO.cleanup()

