from serial import *
from threading import Thread
import io
import time
import json
import urllib

#Load Config Data for this App
try:
	cfg = json.loads(open("config.json").read())
	print cfg

except Exception, e:
	print e
	exit()

def talk_to_pira():
	# Tune to the specified station
	sio.write(unicode(cfg['Stations'][0]['freq']) + "*F")
	sio.flush()
	sio.write(unicode("*E"))
	sio.flush()
	sio.write(unicode("*P"))
	sio.flush()
	sio.write(unicode("?P"))
	sio.flush()

# Create serial connection
ser = Serial(
	port = cfg['serialport'],
	baudrate = cfg['baudrate'],
	bytesize = EIGHTBITS,
	parity = PARITY_NONE,
	stopbits = STOPBITS_ONE,
	timeout = 0.1, 
	xonxoff = 0,
	rtscts = 0,
	#interCharTimeout = None
)


# Create serial connection
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
talk_to_pira()

while True:
	# Receive a line of RDS data from the Pira Decoder serial connection
	line = ser.readlines(1000)
	if(len(line)>0):
		print "Pira says: {0}".format(line)
	
