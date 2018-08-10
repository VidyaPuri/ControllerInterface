from tkinter import *
from tkinter import font
from numpy import interp
import Adafruit_PCA9685
import time
PCA9685_pwm = Adafruit_PCA9685.PCA9685()
PCA9685_pwm.set_pwm_freq(60)

servo_min = [130,170,165,135,340,0]
servo_max = [570,550,480,540,800,0]

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
font = font.Font(weight = "bold",size = 16)

def fun(val):
    val0 = var0.get()
    val1 = var1.get()
    val2 = var2.get()
    val3 = var3.get()
    val4 = var4.get()
    val5 = var5.get()
    val = [val0,val1,val2,val3,val4,val5]
    for i in range(0,6):
        #print(val[i])
        move_servo(i, val[i])

def move_servo(servo,pos):
        print("Servo",servo,"moves to:",pos)
        PCA9685_pwm.set_pwm(servo,0,pos)
        #time.sleep(1)
def reset(val):
    if val == 0:
        scale0.set((servo_min[0]+servo_max[0])/2)
    elif val == 1:
        scale1.set((servo_min[1]+servo_max[1])/2)
    elif val == 2:
        scale2.set((servo_min[2]+servo_max[2])/2)
    elif val == 3:
        scale3.set((servo_min[3]+servo_max[3])/2)
    elif val == 4:
        scale4.set((servo_min[4]+servo_max[4])/2)
    elif val == 5:
        scale5.set((servo_min[5]+servo_max[5])/2)

servo_label0 = Label(root,textvariable = servo0, relief = RAISED,bd=3,font = font)
servo0.set("Servo motor 0")
servo_label0.pack(anchor =W)
scale0 = Scale(root, from_=servo_min[0],to_=servo_max[0],orient=HORIZONTAL,length =300, command=fun, variable = var0)
scale0.pack(anchor =W)
scale0.set((servo_min[0]+servo_max[0])/2)
button0 = Button(root, text = "Pos0 value", command = lambda: reset(0), bd=3)
button0.pack(anchor =W)
label0= Label(root)
label0.pack()

servo_label1 = Label(root,textvariable = servo1, relief = RAISED,bd=3,font = font)
servo1.set("Servo motor 1")
servo_label1.pack(anchor =W)
scale1 = Scale(root, variable = var1,from_=servo_min[1],to_=servo_max[1],orient=HORIZONTAL,length =300)
scale1.pack(anchor =W)
scale1.set((servo_min[1]+servo_max[1])/2)
button1 = Button(root, text = "Pos1 value",command = lambda: reset(1))
button1.pack(anchor =W)
label1= Label(root)
label1.pack()

servo_label2 = Label(root,textvariable = servo2, relief = RAISED,bd=3,font = font)
servo2.set("Servo motor 2")
servo_label2.pack(anchor =W)
scale2 = Scale(root, variable = var2,from_=servo_min[2],to_=servo_max[2],orient=HORIZONTAL,length =300)
scale2.pack(anchor =W)
scale2.set((servo_min[2]+servo_max[2])/2)
button2 = Button(root, text = "Pos2 value",command = lambda: reset(2),bd=3)
button2.pack(anchor =W)
label2= Label(root)
label2.pack()

servo_label3 = Label(root,textvariable = servo3, relief = RAISED,bd=3,font = font)
servo3.set("Servo motor 3")
servo_label3.pack(anchor =W)
scale3 = Scale(root, variable = var3,from_=servo_min[3],to_=servo_max[3],orient=HORIZONTAL,length =300)
scale3.pack(anchor =W)
scale3.set((servo_min[3]+servo_max[3])/2)
button3 = Button(root, text = "Pos3 value",command = lambda: reset(3),bd=3)
button3.pack(anchor =W)
label3= Label(root)
label3.pack()

servo_label4 = Label(root,textvariable = servo4, relief = RAISED,bd=3,font = font)
servo4.set("Servo motor 4")
servo_label4.pack(anchor =W)
scale4 = Scale(root, variable = var4,from_=servo_min[4],to_=servo_max[4],orient=HORIZONTAL,length =300)
scale4.pack(anchor =W)
scale4.set((servo_min[4]+servo_max[4])/2)
button4 = Button(root, text = "Pos4 value",command = lambda: reset(4),bd=3)
button4.pack(anchor =W)
label4= Label(root)
label4.pack()

servo_label5 = Label(root,textvariable = servo5, relief = RAISED,bd=3,font = font)
servo5.set("Servo motor 5")
servo_label5.pack(anchor =W)
scale5 = Scale(root, variable = var5,from_=servo_min[5],to_=servo_max[5],orient=HORIZONTAL,length =300)
scale5.pack(anchor =W)
scale5.set((servo_min[5]+servo_max[5])/2)
button5 = Button(root, text = "Pos5 value",command = lambda: reset(5),bd=3)
button5.pack(anchor =W)
label5= Label(root)
label5.pack()

root.mainloop()