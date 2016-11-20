__author__ = 'teddycool'
#State-switching and handling of general rendering

import time
from Inputs import IoInputs
from Actuators import LedIndicator
#Global GPIO used by all...
import RPi.GPIO as GPIO
from NetflixBridgeConfig import config
from Wan import InternetDetection
import os


class MainLoop(object):
    def __init__(self):
        #TODO: fix logging to file readable from web
        self._gpio = GPIO
        self._gpio.setmode(GPIO.BCM)
        self._resetButton = IoInputs.PushButton(self._gpio, config["IO"]["RedButton"])
        self._internetLed =  InternetDetection.InternetDetection(self._gpio)
        self._resetLed = LedIndicator.LedIndicator(self._gpio, config["IO"]["RedLed"])

        #States: STARTING, RUNNING,  RESETTING



    def initialize(self):
        print "Main init..."
        self.time=time.time()
        self._resetButton.initialize()
        self._internetLed._iLed.activate()
        self._resetLed.activate()
        time.sleep(2) #showing working leds...
        self._internetLed.initialize()



    def update(self):
        start = time.time()
        print "Main update time: " + str(time.time() - start)
        self._internetLed.update()
        #Supersimple statehandling...
        buttonstate = self._resetButton.update()
        if buttonstate == "Pressed":
            self._resetLed.activate()
        if buttonstate == "LongPressed":
            #Make a sudo reboot...
            print os.system('sudo mkdir /tmp/stream')
        if buttonstate == "Released":
            self._resetLed.activate(False)
        time.sleep(config["Main"]["CycleTime"] )


    def __del__(self):
        GPIO.cleanup()