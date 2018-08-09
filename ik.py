
import numpy as np
from math import atan2, cos, sin, pi, sqrt, pow


# DH Table
# Link    a       alpha   d       theta
# 1       a1      -90     d1      *
# 2       a2      0       0       theta2-pi/2
# 3       a3      -90     0       *
# 4       0       -90     d4      *
# 5       0       90      0       *
# 6       0       0       d6      *

a1 = 0.30
a2 = 1.22
a3 = 0.26
d1 = 1.10
d4 = 1.33
d6 = 0.30

# H = np.array([[1,0,0,0.2],
#             [0,1,0,0.2],
#             [0,0,1,0.2],
#             [0,0,0,1]])

def calcFK(th):

    s1 = sin(th[0])
    s2 = sin(th[1]-pi/2)
    s3 = sin(th[2])
    s4 = sin(th[3])
    s5 = sin(th[4])
    s6 = sin(th[5])

    c1 = cos(th[0])
    c2 = cos(th[1]-pi/2)
    c3 = cos(th[2])
    c4 = cos(th[3])
    c5 = cos(th[4])
    c6 = cos(th[5])

    A1 = np.array([[c1,0,-s1,a1*c1],
                   [s1,0,c1,a1*s1],
                   [0,-1,0,d1],
                   [0,0,0,1]])

    A2 = np.array([[c2,-s2,0,a2*c2],
                   [s2,c2,0,a2*s2],
                   [0,0,1,0],
                   [0,0,0,1]])


    A3 = np.array([[c3,0,-s3,a3*c3],
                   [s3,0,c3,a3*s3],
                   [0,-1,0,0],
                   [0,0,0,1]])

    A4 = np.array([[c4,0,-s4,0],
                   [s4,0,c4,0],
                   [0,-1,0,d4],
                   [0,0,0,1]])

    A5 = np.array([[c5,0,s5,0],
                   [s5,0,-c5,0],
                   [0,1,0,0],
                   [0,0,0,1]])

    A6 = np.array([[c6,-s6,0,0],
                   [s6,c6,0,0],
                   [0,0,1,d6],
                   [0,0,0,1]])

    R1 = A1[0:3,0:3]
    R2 = A2[0:3,0:3]
    R3 = A3[0:3,0:3]

    R03 = R1 @ R2 @ R3
    #print(R03)
    A = A1 @ A2 @ A3 @ A4 @ A5 @ A6

    #print(A)
    return(A,R03)



def rot2eul(R):


    r13 = R[0,2]
    r23 = R[1,2]
    r33 = R[2,2]
    r31 = R[2,0]
    r32 = R[2,1]

    sy = sqrt(1-pow(r33, 2))

    y1 = atan2(sy, r33)
    y2 = atan2(-sy, r33)

    if sy > 0:
        x = atan2(r23, r13)
        z = atan2(r32, -r31)
    elif sy < 0:
        x = atan2(-r23, -r13)
        z = atan2(-r32, r31)
    elif sy == 0:
        sy = 0.001
        y1 = 0.0
        r31 = 0.0
        x = atan2(r23, r13)
        z = atan2(r32, -r31)-pi         # not sure why this -pi has to be here - singularities

    return x,y1,z

def calcIK(H):
    #print(H)
    O = H[:,3]
    Oc = O - d6*H[:,2]

    rx = Oc[0]
    ry = Oc[1]
    rz = Oc[2]

    theta1 = atan2(Oc[1],Oc[0])
    theta1_deg = theta1*180/pi

    px = sqrt(pow(rx,2)+pow(ry,2))-a1
    py = rz - d1
    r = sqrt(pow(px,2)+pow(py,2))
    sd = sqrt(pow(a3,2)+pow(d4,2))
    D1 = (pow(a2,2)+pow(r,2)-pow(sd,2))/(2*a2*r)
    D2 = (pow(a2, 2) + pow(sd, 2) - pow(r, 2)) / (2 * a2 * sd)

    xi = atan2(d4,a3)
    alfa = atan2(py,px)
    print('D1',D1,'D2',D2)
    beta = atan2(sqrt(1-pow(D1,2)),D1)
    gama = atan2(sqrt(1-pow(D2,2)),D2)

    theta2 = pi/2 - (alfa+beta)
    theta2_deg = theta2*180/pi

    theta3 = -(gama+xi -pi)
    theta3_deg = theta3*180/pi

    th03 = [theta1,theta2,theta3,0,0,0]
    th_deg = [theta1_deg,theta2_deg,theta3_deg]

    [empty, R03] =calcFK(th03)

    R = H[0:3,0:3]
    R36 = R03.transpose() @ R
    #print('R36',R36)
    [x,y,z] = rot2eul(R36)

    theta1 = round(theta1, 4)
    theta4 = round(x, 4)
    theta5 = round(y, 4)
    theta6 = round(z, 4)
    print(theta4 + theta6)
    if abs(theta4 + theta6) < 0.1:   # remove rotations in oposite sides
        theta4 = 0
        theta6 = 0
    elif theta4 == theta6:
        theta4 = 0
        theta6 = 0
    th = [theta1, theta2, theta3 - theta2, theta4, theta5, theta6]
    print(th)
    return th

