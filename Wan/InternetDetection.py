__author__ = 'teddycool'
#http://stackoverflow.com/questions/17304225/how-to-detect-if-computer-is-contacted-to-the-internet-with-python
#Handle check of internetconnection and turning on/off a indication led
import os
import time
import urllib2
from Actuators import LedIndicator
try:
    from NetflixBridgeConfig import config
except:
    config = {
              "InternetDetection": {"URL": "http://www.google.com","TimeSlot":1}, #Used when testing this module
              }

class InternetDetection(object):

    def __init__(self, gpio):
        print "Init"
        self._lastCheck = 0 #Force check at first update
        self._iLed = LedIndicator.LedIndicator(gpio, config["IO"]["GreenLed"])
        self._connected = "Not connected"


    def initialize(self):
        print "Initialize"
        self._iLed.activate(False)


    def update(self):
        if time.time() - self._lastCheck > config["InternetDetection"]["TimeSlot"]:
            try:
                urllib2.urlopen(config["InternetDetection"]["URL"]).close()
                self._connected = "Connected"
                self._iLed.activate(True)
                self._lastCheck = time.time()
            except:
                self._connected = "Not connected"
                self._iLed.activate(False)
        return self._connected

    def __del__(self):
        self._iLed.activate(False)
        return


if __name__ == '__main__':
    print "Testcode for NetDetector"
    nd = InternetDetection()
    nd.initialize()
    while(True):
        nd.update()
        time.sleep(1)