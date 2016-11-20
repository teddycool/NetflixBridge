__author__ = 'teddycool'

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
        time.sleep(2) #showing that leds are working at startup...
        self._internetLed.initialize()


    def update(self):
        start = time.time()
        print "Main update time: " + str(time.time() - start)
        print self._internetLed.update()
        #Supersimple statehandling...
        buttonstate = self._resetButton.update()
        print buttonstate
        if buttonstate == "Pressed":
            self._resetLed.activate()
        if buttonstate == "LongPressed":
            #Make a sudo reboot...
            print "Rebooting...."
            self._resetLed.activate(False)
            self._internetLed._iLed.activate(False)
            os.system('sudo reboot')
        if buttonstate == "Released":
            self._resetLed.activate(False)
        time.sleep(config["Main"]["CycleTime"] )


    def __del__(self):
        GPIO.cleanup()