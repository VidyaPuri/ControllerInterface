#from tkinter import *
#from tkinter import font
#from numpy import interp
#import Adafruit_PCA9685
import time
import x360
#PCA9685_pwm = Adafruit_PCA9685.PCA9685()
#PCA9685_pwm.set_pwm_freq(60)

servoMin = [130,170,145,135,130,170]
servoMax = [570,550,390,540,650,650]

contMin =[-100,-100,-100,-100,-100,-100]
contMax =[100,100,100,100,100,100]

startPos =[350,360,325,340,500,300]
currentPos = startPos
posEx = [0]*6
# #root = Tk()
# var0 = DoubleVar()
# var1 = DoubleVar()
# var2 = DoubleVar()
# var3 = DoubleVar()
# var4 = DoubleVar()
# var5 = DoubleVar()
# servo0 = StringVar()
# servo1 = StringVar()
# servo2 = StringVar()
# servo3 = StringVar()
# servo4 = StringVar()
# servo5 = StringVar()
ifGrad = False
running = True
digStep = 10
command = ""
step=1
poz = 0
moveVals ={"X1":0,"Y1":0,"X2":0,"Y2":0,"dpadU":1,"dpadD":1,"dpadL":1,"dpadR":1}
slovar ={}
id = 0
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
    global ifGrad,command,poz,id
    #if controlId not in slovar:
        #slovar.update({'controlId':Value})
    id = xboxCont.controlValues[controlId]
    command = controlId
    poz = getattr(xboxCont,command)
    # if you press guide - control mode changes
    if xboxCont.startBut == 1:
        running = True
    if xboxCont.guideBut == 1:
        ifGrad = not ifGrad
        init()
    # if not k == "":
    #     move()
    # if controlId in moveVals:
    #     # gradient mode
    #     if ifGrad == True:
    #         moveGrad(controlId,id,Value)
    #     # normal mode
    #     elif ifGrad == False and id<=3:
    #         servoPos = mapFromTo(Value,contMin[id],contMax[id],servoMin[id],servoMax[id])
    #         servoPos = int(servoPos)
    #         moveServo(id,servoPos)

def moveServo(id,pos):
        print("Servo",id,"moves to:",pos)
        #PCA9685_pwm.set_pwm(id,0,pos)

def moveGrad(controlId,id,pos):
    # analog = 0 and digital = 1
    if moveVals[controlId]==0:
        # it is more convenient this way
        if id == 2:
            id = 3
        elif id == 3:
            id = 2
        print("this is analog")
        currentPos[id] = currentPos[id]+ pos*step
        #max limit
        if currentPos[id]>=servoMax[id]:
            currentPos[id] = servoMax[id]
        #min limit
        elif currentPos[id]<=servoMin[id]:
            currentPos[id]=servoMin[id]
        currentPos[id] = int(currentPos[id])
    # digital = 1
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
    #PCA9685_pwm.set_pwm(id,0,currentPos[id])

init()

xboxCont = x360.Joystick(controllerCallBack = myCallBack)
try:
    xboxCont.start()
    print("xbox controller running")
except KeyboardInterrupt:
    print("user canceled")
    running = False
    xboxCont.stop()

# while running == True:
#
#     currentPos[id] = currentPos[id] + poz*step
#     print("currentPos:",currentPos[id])
#     time.sleep(0.05)
# def test():
#     while running ==True:
#         print(id,poz)
while running == True:
    if not command == "":
        if command in moveVals:
            #analog
            if moveVals[command]==0:
                # it is more convenient this way
                if id == 2:
                    id = 3
                elif id == 3:
                    id = 2
                #print("poz:",poz,"command",command,"id:",id)
                currentPos[id] = currentPos[id] + poz*step
                #max limit
                if currentPos[id]>=servoMax[id]:
                    currentPos[id] = servoMax[id]
                #min limit
                elif currentPos[id]<=servoMin[id]:
                    currentPos[id]=servoMin[id]
                currentPos[id] = int(currentPos[id])
        # digital = 1
            elif moveVals[command] == 1:

                if command == "dpadU":
                    id = 4
                    currentPos[id]=currentPos[id]+digStep*poz
                    if currentPos[id]>=servoMax[id]:
                        currentPos[id] = servoMax[id]
                elif command == "dpadD":
                    id = 4
                    currentPos[id]=currentPos[id]-digStep*poz
                    if currentPos[id]<=servoMin[id]:
                        currentPos[id] = servoMin[id]
                elif command == "dpadL":
                    id = 5
                    currentPos[id]=currentPos[id]+digStep*poz
                    if currentPos[id]>=servoMax[id]:
                        currentPos[id] = servoMax[id]
                elif command =="dpadR":
                    id = 5
                    currentPos[id]=currentPos[id]-digStep*poz
                    if currentPos[id]<=servoMin[id]:
                        currentPos[id] = servoMin[id]
            print("currentPos",currentPos[id],command)
            #PCA9685_pwm.set_pwm(id,0,currentPos[id])

        time.sleep(0.05)
