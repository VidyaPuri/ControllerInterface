#import subprocessXbox
import xbox360
import time

joy = xbox360.Joystick()

if joy.connected():
    print("connected")
else:
    print("disconnected")

while not joy.Back():

    print("time:",time.time(),"Lx",joy.leftX(),"Ly",joy.leftY(),"Lx",joy.leftX(),"Rx",joy.rightX(),
    "Ry",joy.rightY(),"A",joy.A())
    #time.sleep(1)

    if joy.leftY():
        print("Ly",joy.leftY())

    if joy.A():
        print("A",joy.A())

"""    if joy.B():
        print "B",
    else:
        print " ",
    if joy.X():
        print "X",
    else:
        print " ",
    if joy.Y():
        print "Y",
    else:
        print " ",
    # Dpad U/D/L/R
    print "Dpad ",
    if joy.dpadUp():
        print "U",
    else:
        print " ",
    if joy.dpadDown():
        print "D",
    else:
        print " ",
    if joy.dpadLeft():
        print "L",
    else:
        print " ",
    if joy.dpadRight():
        print "R",
    else:
        print " ",
"""

joy.close()
