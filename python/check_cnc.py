# Importing Libraries
import serial
import time
import math
import os
import time
import hashlib
import traceback
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)
start = 1
from gpiozero import LED
import RPi.GPIO as GPIO
from signal import pause
try:
   int('')
except ValueError:
   pass      # or whatever

def write_read(num):
    arduino.write("\r\n\r\n".encode('utf-8')+num.encode('utf-8')+"\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
def alphabetical_value(str):
    return 'abcdefghijklmnopqrstuvwxyz'.index(str.lower()) + 1

def cnc1(x,y):
    XSUM = 0
    YSUM = 0
    cube = 43
    Delay_time=0
    #half_cube=cube/2
    arduino.write("\r\n\r\n".encode('utf-8') + "$X".encode('utf-8') + "\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data.decode('utf-8'))
    arduino.write("\r\n\r\n".encode('utf-8') + "$".encode('utf-8') + "\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data.decode('utf-8'))
    arduino.write("\r\n\r\n".encode('utf-8') + "$".encode('utf-8') + "\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data.decode('utf-8'))
    arduino.write("\r\n\r\n".encode('utf-8') + "$".encode('utf-8') + "\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data.decode('utf-8'))
    arduino.write("\r\n\r\n".encode('utf-8') + "$X".encode('utf-8') + "\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    print(data.decode('utf-8'))
    start=0

    XSTART = x % 10
    YSTART = x // 10
    XEND=y%10
    YEND=y//10
    Xstep=cube*(XSTART)
    Ystep=cube*(YSTART)
    XSUM+= Xstep
    YSUM+= Ystep
    print("Y STEP VALUE",Ystep)
    #A2TOB3
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    print(Ystep)
    value = write_read(num)
    print(value.decode('utf-8'))
    print(Xstep)
    Delay_time=math.sqrt((XSTART*3)**2+(YSTART*3)**2)
    time.sleep(Delay_time)#move to cordinate

    num = '$J=G21G91X' + str(-XSUM) + 'Y' + str(-YSUM) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    print(XSUM)
    print(YSUM)
    Delay_time=math.sqrt(int(((XSUM/cube)*3)**2)+((YSUM)/cube*3)**2)
    time.sleep(Delay_time)
    XSUM=0
    YSUM=0
    
    return

while True:
    x=input("enter x")
    y=input("enter y")
    cnc1(int(x),int(y))