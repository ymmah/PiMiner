#!/usr/bin/python

import sys, subprocess, time, urllib2, socket
sys.path.append("/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_CharLCDPlate")
from Adafruit_CharLCD import Adafruit_CharLCDPlate
import Adafruit_CharLCD as LCD
from PiMinerDisplay import PiMinerDisplay

HOLD_TIME	= 3.0 #Time (seconds) to hold select button for shut down
REFRESH_TIME= 3.0 #Time (seconds) between data updates
HALT_ON_EXIT= True
display		= PiMinerDisplay()
lcd			= display.lcd
prevCol		= -1
prev		= ""
lastTime	= time.time()

def shutdown():
	lcd.clear()
	if HALT_ON_EXIT:
		lcd.message('Wait 30 seconds\nto unplug...')
		subprocess.call("sync")
		subprocess.call(["shutdown", "-h", "now"])
	else:
		exit(0)

'''
#WIP - startup on boot
def internetOn():
	try:
		response=urllib2.urlopen('http://google.com',timeout=3)
		return True
	except urllib2.URLError as err:
		pass
	return False
'''

#Check for network connection at startup
t = time.time()
while True:
	lcd.clear()
	lcd.message('checking network\nconnection (' + str(int(time.time() - t)) + 's)...')
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 0))
		lcd.set_color(1.0, 1.0, 1.0)
		lcd.clear()
		lcd.message('IP address:\n' + s.getsockname()[0])
		time.sleep(5)
		display.initInfo()	# Start info gathering/display
		break         		# Success
	except:
		time.sleep(1) 		# Pause a moment, keep trying
'''
	if internetOn() == True:
		time.sleep(5)
		break         # Success
	else:
		time.sleep(1) # Pause a moment, keep trying
'''

buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (1,0,1)) )

# Listen for button presses
while True:
	b = ""
	for button in buttons:
		if lcd.is_pressed(button[0]):
			b += button[1]
	if b != prev:
		if lcd.is_pressed(LCD.SELECT):
			tt = time.time()                        # Start time of button press
			while lcd.is_pressed(LCD.SELECT):	# Wait for button release
				if (time.time() - tt) >= HOLD_TIME: # Extended hold?
					shutdown()						# We're outta here
			display.backlightStep()
		elif lcd.is_pressed(LCD.LEFT):
	  		display.scrollRight()
		elif lcd.is_pressed(LCD.RIGHT):
			display.scrollLeft()
		elif lcd.is_pressed(LCD.UP):
			display.modeUp()
		elif lcd.is_pressed(LCD.DOWN):
			display.modeDown()
		prev = b
		lastTime = time.time()
	else:
		now = time.time()
		since = now - lastTime
		if since > REFRESH_TIME or since < 0.0:
			display.update()
			lastTime = now
