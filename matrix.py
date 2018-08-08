import numpy as np
import copy
from math import cos, sin, pi
degAngles = []
#degAngle = 0
def rad2deg(angles):
    if isinstance(angles, list):                # for lists and single values
        for i, val in enumerate(angles):
            degAngles.append(val*180/pi)
    else:
        dA = angles*180/pi
        return dA
    return degAngles

def deg2rad(angles):
    if isinstance(angles, list):                # for lists and single values
        for i, val in enumerate(angles):
            degAngles.append(val*pi/180)
    else:
        dA = angles*pi/180
        return dA
    return degAngles

def calcMatrix(moveVector):
    x = moveVector[0]
    y = moveVector[1]
    z = moveVector[2]
    a = deg2rad(moveVector[3])
    b = deg2rad(moveVector[4])
    c = deg2rad(moveVector[5])

    sA = sin(a)
    sB = sin(b)
    sC = sin(c)
    cA = cos(a)
    cB = cos(b)
    cC = cos(c)

    transX = np.array([[1,0,0,x],
                        [0,1,0,0],
                        [0,0,1,0],
                        [0,0,0,1]])

    transY = np.array([[1,0,0,0],
                        [0,1,0,y],
                        [0,0,1,0],
                        [0,0,0,1]])

    transZ = np.array([[1,0,0,0],
                        [0,1,0,0],
                        [0,0,1,z],
                        [0,0,0,1]])

    rotR = np.array([[1,0,0,0],             # roll
                    [0,cA,-sA,0],
                    [0,sA,cA,0],
                    [0,0,0,1]])

    rotP = np.array([[cB,0,sB,0],           # pitch
                    [0,1,0,0],
                    [-sB,0,cB,0],
                    [0,0,0,1]])

    rotJ = np.array([[cC,-sC,0,0],          # jaw
                    [sC,cC,0,0],
                    [0,0,1,0],
                    [0,0,0,1]])


    M = transX @ transY @ transZ @ rotR @ rotP @ rotJ
    #print(np.round_(M,4))
    return M
# x = 0.2
# y = 0
# z = 0.2
# degA = 90
# degB= 90
# degC = 90
#
# a = deg2rad(degA)
# b = deg2rad(degB)
# c = deg2rad(degC)
#
# calcMatrix(x, y, z, a, b, c)