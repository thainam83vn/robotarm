import serial
import time

ser = serial.Serial('COM4')
for i in range(0,4):
	ser.write(b'1+\n')
	time.sleep(0.2)

ser.close()