__author__ = 'teddycool'


import MainLoop
import time


class Main(object):

    def __init__(self):
        print "Init Main object for NetBridgeLogger..."
        self._mainLoop=MainLoop.MainLoop()


    def run(self):
        self._mainLoop.initialize()
        stopped = False
        while not stopped:
            self._mainLoop.update()
            time.sleep(0.01)



if __name__ == "__main__":
    cd=Main()
    cd.run()


#Put in  /etc/rc.local for autostart at boot:
#cd /home/pi/NetflixBridge
#sudo python Main.py &