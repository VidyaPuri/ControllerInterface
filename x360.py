import subprocess
import time
import os
import threading
import re

class Joystick(threading.Thread):

    def __init__(self,controllerCallBack = None,deadzone=0):
        threading.Thread.__init__(self)
        self.controllerCallBack = controllerCallBack
        self.proc = subprocess.Popen(['xboxdrv','--no-uinput','--detach-kernel-driver'], stdout=subprocess.PIPE, bufsize = 1, universal_newlines=True)
        self.pipe = self.proc.stdout
        found = False
        waitTime = time.time() + 3
        while waitTime > time.time() and not found:
            response = self.pipe.readline()
            #hard fail, force error
            if response[0:7] == "No Xbox":
                raise IOError("No Xbox controller/receiver found")
            #success if we see following
            if response[0:12].lower() == ("press ctrl-c"):
                found = True
            if len(response) == 140:
                found = True
                self.connectStatus = True
                self.reading = response
        if not found:
            self.close()
            raise IOError("Unable to detect Xbox controller - Try sudo")
        print("Initialisation completed")

        # flag for thread running
        self.running = False

        # initialisation of controlValues
        self.controlValues = {"X1":0,
                            "Y1":1,
                            "X2":2,
                            "Y2":3,
                            "dpadU":4,
                            "dpadD":5,
                            "dpadL":6,
                            "dpadR":7,
                            "backBut":8,
                            "guideBut":9,
                            "startBut":10,
                            "lThumb":11,
                            "rThumb":12,
                            "A":13,
                            "B":14,
                            "X":15,
                            "Y":16,
                            "lBump":17,
                            "rBump":18,
                            "lTrig":19,
                            "rTrig":20}

        #initializing of controlVariables
        for k,v in self.controlValues.items():
            setattr(self,k,0)

# end of initialization

    def run(self):
        self._start()

    def doCallBacks(self, control, value):

        #call the general callback
        if self.controllerCallBack != None: self.controllerCallBack(control, value)

    def _start(self):
        self.running = True

        # reading raw values out of xboxdrv input string
        while(self.running):
            for line in self.pipe:

                # reg exp parses the values out of raw xboxdrv input string
                values=re.findall(":\s*(-?\d+)",line)
                for k,v in self.controlValues.items():
                    value = int(values[v])

                    #only the analog sticks values need scaling and deadzone adj
                    if k == "X1" or k == "Y1" or k == "X2" or k == "Y2":
                        value = float("{0:.4f}".format(self.axisScale(value)))
                    # values that change must be passed to doCallBacks
                    if not getattr(self,k) == value:
                        setattr(self,k,value)
                        self.doCallBacks(k,getattr(self,k))

    # scaling and deadzone adjustment for analog sticks
    def axisScale(self,raw,deadzone = 6000):
        if abs(raw) < deadzone:
            return 0.0
        else:
            if raw < 0:
                return (raw + deadzone) / (32786.0 - deadzone)*100
            else :
                return (raw - deadzone) / (32786.0 - deadzone)*100

    def close(self):
        os.system('pkill xboxdrv')

    def stop(self):
        self.running = False
