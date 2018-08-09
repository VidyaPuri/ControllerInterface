import Adafruit_PCA9685
import time
import x360
PCA9685_pwm = Adafruit_PCA9685.PCA9685()
PCA9685_pwm.set_pwm_freq(60)

from tkinter import *
from tkinter import font

import ik
import copy
import matrix
import numpy as np


servoMin = [130,170,145,135,130,170]
servoMax = [570,550,390,540,650,650]

#contMin =[-100,-100,-100,-100,-100,-100]
#contMax =[100,100,100,100,100,100]

#startPos =[350,360,325,340,500,300]
startPos =[0,0,0,0,0,0]
initPos = [0,0,0,0,0,0]
#x = 5
#goToPos = copy.deepcopy(startPos)
moveVector = [0,0,0,0,0,0]


def mapFromTo(x,a,b,c,d): #maps range from a - b = input range c - d = output range x -value
    y=(x-a)/(b-a)*(d-c)+c

    return y

def gogo(pos):
    for i in range(0, 6):
        pos[i] = int(pos[i])
        pos[i] = mapFromTo(pos[i],-90,90,servoMin[i],servoMax[i])
        move(i, pos[i])

def move(servoNo,pos):
    PCA9685_pwm.set_pwm(servoNo,0, int(pos))
    print('Servo:', servoNo, 'is at:',int(pos))

#
# def main():
#
#     # moveVector[0] = 0.5
#     # moveVector[1] = 0.9
#     # moveVector[2] = -0.3
#     moveVector[3] = 0
#     moveVector[4] = 0
#     moveVector[5] = 0
#     # print('moveVector', moveVector)
#     while True:
#         degAngle = []
#         try:
#             print('Vnesi x')
#             x = float(input())
#             print('x:',x)
#             print('Vnesi y')
#             y = float(input())
#             print('y:',y)
#             print('Vnesi z')
#             z = float(input())
#             print('z:',z)
#         except ValueError:
#             print("Invalid input.")
#         moveVector[0] = x
#         moveVector[1] = y
#         moveVector[2] = z
#         print('moveVector',moveVector)
#         M = matrix.calcMatrix(moveVector)
#         print(np.round_(M, 4), '\n')
#
#         Vector = [startPos[0], startPos[1], startPos[2], startPos[3], startPos[4], startPos[5]]
#         #print('Vector',Vector)
#         [A, RR] = ik.calcFK(Vector)
#         newA = M @ A
#         theta = ik.calcIK(newA)
#         #print('Vector:',startPos,'\n')
#
#         print(np.round_(A,4),'\n')
#         print(np.round_(newA, 4),'\n')
#         print('theta',theta)
#         # [B, BB] = ik.calcFK(theta)
#         # print(np.round_(B, 4))
#         degAngle = matrix.rad2deg(theta)
#         print('degAngle', degAngle)
#         goToPos = degAngle
#         print(goToPos)
#
#         gogo(goToPos)
#         del degAngle[:]
#
# print('startPos',startPos)
# gogo(initPos)
# main()

top = Tk()



l = Label(top, text='')
def reset():
    s1.set(0)
    s2.set(0)
    s3.set(0)

def show(val):
    label1.config(text='x: ' +str(val1.get()))
    label2.config(text='y: ' +str(val2.get()))
    label3.config(text='z: ' + str(val3.get()))

def translation(val):
    label1.config(text='x: ' + str(val1.get()))
    label2.config(text='y: ' + str(val2.get()))
    label3.config(text='z: ' + str(val3.get()))
    x = val1.get()
    y = val2.get()
    z = val3.get()
    moveVector[0] = x
    moveVector[1] = y
    moveVector[2] = z
    moveVector[3] = 0.0
    moveVector[4] = 0.0
    moveVector[5] = 0.0
    #print(moveVector)
    M = matrix.calcMatrix(moveVector)
    #print(np.round_(M, 4), '\n')

    Vector = [startPos[0], startPos[1], startPos[2], startPos[3], startPos[4], startPos[5]]
    [A, RR] = ik.calcFK(Vector)
    newA = M @ A
    theta = ik.calcIK(newA)
    print(np.round_(newA, 4), '\n')
    print('theta', theta)
    degAngle = matrix.rad2deg(theta)
    print('degAngle', np.round_(degAngle, 4))
    # print(goToPos)
    gogo(degAngle)
    del degAngle[:]


val1 = DoubleVar()
val2 = DoubleVar()
val3 = DoubleVar()


s1 = Scale(top, from_= -1.0, to=1.0, resolution=0.05, orient=HORIZONTAL, length=300, command=translation, variable=val1)
s1.set(0)
s2 = Scale(top, from_= -1.0, to=1.0, resolution=0.05, orient=HORIZONTAL, length=300, command=translation, variable=val2)
s2.set(0)
s3 = Scale(top, from_= -1.0, to=1.0, resolution=0.05, orient=HORIZONTAL, length=300, command=translation, variable=val3)
s3.set(0)
button0 = Button(top, text="Reset", command=reset)
button0.pack(anchor=N)

s1.pack()
s2.pack()
s3.pack()
label1 = Label(top)
label1.pack()
label2 = Label(top)
label2.pack()
label3 = Label(top)
label3.pack()


top.mainloop()

