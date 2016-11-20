
#from LoggerConfig import deviceconfig
from Actuators import LedIndicator
from  NetflixBridgeConfig import config


import RPi.GPIO as GPIO
import time

#Start...
GPIO.setmode(GPIO.BCM)
leds = []
for led in config["IO"]:
    leds.append(LedIndicator.LedIndicator(GPIO, config["IO"][led]))

print "Start testing...."

running = True
ligth = True
while(running):
    try:
        for led in leds:
            led.activate(ligth)
            time.sleep(0.1)
        ligth = not ligth
    except:
        running= False
for led in leds:
    del(led)
GPIO.cleanup()
print "Test is done..."






