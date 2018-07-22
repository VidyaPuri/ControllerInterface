from tkinter import *
from tkinter import font
from numpy import interp
import Adafruit_PCA9685
import time
import x360
PCA9685_pwm = Adafruit_PCA9685.PCA9685()
PCA9685_pwm.set_pwm_freq(60)

servoMin = [130,170,165,135,340,200]
servoMax = [570,550,480,540,800,500]

contMin =[-100,-100,0,-100,-100,0]
contMax =[100,100,100,100,100,100]

startPos =[350,360,325,340,500,0]
currentPos = startPos
root = Tk()
var0 = DoubleVar()
var1 = DoubleVar()
var2 = DoubleVar()
var3 = DoubleVar()
var4 = DoubleVar()
var5 = DoubleVar()
servo0 = StringVar()
servo1 = StringVar()
servo2 = StringVar()
servo3 = StringVar()
servo4 = StringVar()
servo5 = StringVar()
ifGrad = False
digStep = 50
step=0.05
moveVals ={"X1":0,"Y1":0,"X2":0,"Y2":0,"dpadU":1,"dpadD":1,"dpadL":1,"dpadR":1}

#font = font.Font(weight = "bold",size = 16)
def init():
    print("Initialisation, robot goes to mid position on all servos")
    for i in range(0,5):
        moveServo(i,startPos[i])
        print("Servo",i,"is at pos",startPos[i])

def mapFromTo(x,a,b,c,d): #maps range from a - b = input range c - d = output range
    y=(x-a)/(b-a)*(d-c)+c
    return y

def myCallBack(controlId,Value):
    global ifGrad
    id = xboxCont.controlValues[controlId]

    # if you press guide - control mode changes
    if xboxCont.guideBut == 1:
        ifGrad = not ifGrad
        init()
    if controlId in moveVals:
        # gradient mode
        if ifGrad == True:
            moveGrad(controlId,id,Value)
        # normal mode
        elif ifGrad == False and id<=3:
            servoPos = mapFromTo(Value,contMin[id],contMax[id],servoMin[id],servoMax[id])
            servoPos = int(servoPos)
            moveServo(id,servoPos)

def moveServo(servo,pos):
        print("Servo",servo,"moves to:",pos)
        #PCA9685_pwm.set_pwm(servo,0,pos)

def moveGrad(controlId,id,pos):
    if moveVals[controlId]==0:
        print("this is analog")
        currentPos[id] = currentPos[id]+ pos*step
        #max limit
        if currentPos[id]>=servoMax[id]:
            currentPos[id] = servoMax[id]
        #min limit
        elif currentPos[id]<=servoMin[id]:
            currentPos[id]=servoMin[id]
        currentPos[id] = int(currentPos[id])
            #print("Servo",servo,"moves to:",currentPos[servo])
    elif moveVals[controlId] == 1:

        if controlId == "dpadU":
            id = 4
            currentPos[id]=currentPos[id]+digStep
            if currentPos[id]>=servoMax[id]:
                currentPos[id] = servoMax[id]
        elif controlId == "dpadD":
            id = 4
            currentPos[id]=currentPos[id]-digStep
            if currentPos[id]<=servoMin[id]:
                currentPos[id] = servoMin[id]
        elif controlId == "dpadL":
            id = 5
            currentPos[id]=currentPos[id]+digStep
            if currentPos[id]>=servoMax[id]:
                currentPos[id] = servoMax[id]
        elif controlId =="dpadR":
            id = 5
            currentPos[id]=currentPos[id]-digStep
            if currentPos[id]<=servoMin[id]:
                currentPos[id] = servoMin[id]
        print("this is digital")
    print("Servo",id,"moves to:",currentPos[id])
    PCA9685_pwm.set_pwm(id,0,currentPos[servo])
init()

xboxCont = x360.Joystick(controllerCallBack = myCallBack)
try:
    xboxCont.start()
    print("xbox controller running")
except KeyboardInterrupt:
    print("user canceled")
    xboxCont.stop()
