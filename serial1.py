import serial
import time
RANGE = [[0,0],[0,100],[0,180],[0,180],[0,180],[0,180],[0,180]]
ser=serial.Serial('/dev/ttyUSB0')
ip = 6
i = 0
d = True
while True:
	if d==True:
		i=i+5
		ser.write('6+\n')
	if d==False:
		i=i-5
		ser.write('6-\n')	
	print('Pos:',ip, i)
	time.sleep(0.2)
	if i<=RANGE[ip][0]:
		d=True
	if i>=RANGE[ip][1]:
		d=False

ser.close()
