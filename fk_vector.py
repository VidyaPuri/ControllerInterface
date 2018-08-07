#import Adafruit_PCA9685
import time
import x360
#PCA9685_pwm = Adafruit_PCA9685.PCA9685()
#PCA9685_pwm.set_pwm_freq(60)

servoMin = [130,170,145,135,130,170]
servoMax = [570,550,390,540,650,650]

#contMin =[-100,-100,-100,-100,-100,-100]
#contMax =[100,100,100,100,100,100]

#startPos =[350,360,325,340,500,300]
startPos =[0,0,0,0,0,0]
currentPos = startPos

def mapFromTo(x,a,b,c,d): #maps range from a - b = input range c - d = output range x -value
    y=(x-a)/(b-a)*(d-c)+c
    return y

def init():

    for i in range(0, 5):
        startPos[i] = mapFromTo(startPos[i],-90,90,servoMin[i],servoMax[i])
        move(i, startPos[i])

def move(servoNo,pos):
    #PCA9685_pwm.set_pwm(servoNo,0, pos)
    print('Servo:', servoNo, 'is at:',pos)

init()