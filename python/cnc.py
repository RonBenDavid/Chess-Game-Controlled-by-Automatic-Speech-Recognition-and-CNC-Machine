# Importing Libraries
import serial
import time
import os
import time
import math
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
led = LED(4)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(21, GPIO.OUT)           # set GPIO24 as an output   

def write_read(num):
    arduino.write("\r\n\r\n".encode('utf-8')+num.encode('utf-8')+"\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
def alphabetical_value(str):
    return 'abcdefghijklmnopqrstuvwxyz'.index(str.lower()) + 1

def cnc1(x,y):
    led.on()
    XSUM = 0
    YSUM = 0
    cube = 42
    half_cube=cube/2
    Delay_time=0
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
    
    GPIO.output(21, 0)
    XSTART = x % 8
    YSTART = x // 8
    XEND=y%8
    YEND=y//8
    Xstep=cube*(XSTART)
    Ystep=cube*(YSTART)
    XSUM+= Xstep
    YSUM+= Ystep
    print("Y STEP VALUE",Ystep)
    #A2TOB3
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    Delay_time=(Xstep+Ystep)/cube+5
    time.sleep(Delay_time)#move to cordinate
    
    GPIO.output(21, 1)#enbale electro
    XSUM+= half_cube
    num = '$J=G21G91X' + str(half_cube) + 'Y' + str(0) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    Delay_time=half_cube/cube+5
    time.sleep(Delay_time)#move right half
    
    Xstep=0
    Ystep=cube*(YEND-YSTART)-half_cube
    YSUM+= Ystep
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    Delay_time=(Xstep+Ystep)/cube+5
    time.sleep(Delay_time)#GO UP
    
    Ystep=0
    Xstep=cube*(XEND-XSTART)
    XSUM+= Xstep
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    Delay_time=(Xstep+Ystep)/cube+5
    time.sleep(Delay_time)#GO LEFT OR RIGHT
    
    XSUM+=-half_cube
    YSUM+= half_cube
    num = '$J=G21G91X' + str(-half_cube) + 'Y' + str(+half_cube) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    Delay_time=(half_cube+half_cube)/cube+7
    time.sleep(Delay_time)#move left half
    
    GPIO.output(21, 0)#disable electro
    
    Xstep=cube*(XEND-XSTART)
    Ystep=0
    XSUM+= Xstep
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    Delay_time=(Xstep+Ystep)/cube+5
    time.sleep(Delay_time)

    num = '$J=G21G91X' + str(-XSUM) + 'Y' + str(-YSUM) + 'F10000'
    print(num)
    value = write_read(num)
    print(value.decode('utf-8'))
    Delay_time=(XSUM+YSUM)/cube+5
    time.sleep(Delay_time)
    XSUM=0
    YSUM=0
    led.off()
    return

def hashfile(file):
    # A arbitrary (but fixed) buffer
    # size (change accordingly)
    # 65536 = 65536 bytes = 64 kilobytes
    BUF_SIZE = 65536

    # Initializing the sha256() method
    sha256 = hashlib.sha256()

    # Opening the file provided as
    # the first commandline argument
    with open(file, 'rb') as f:

        while True:

            # reading data = BUF_SIZE from
            # the file and saving it in a
            # variable
            data = f.read(BUF_SIZE)

            # True if eof = 1
            if not data:
                break

            # Passing that data to that sh256 hash
            # function (updating the function with
            # that data)
            sha256.update(data)

    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return sha256.hexdigest()

count=0
# Calling hashfile() function to obtain hashes
# of the files, and saving the result
# in a variable
f1_hash = hashfile("x.txt")
f3_hash = hashfile("y.txt")
while True:
    f2_hash = hashfile("x.txt")
    f4_hash = hashfile("y.txt")
    # Doing primitive string comparison to
    # check whether the two hashes match or not
    if (f1_hash == f2_hash) and (f3_hash == f4_hash):
        continue
    else:
        print("Files are different!")
        print(f"Hash of File 1: {f1_hash}")
        print(f"Hash of File 2: {f2_hash}")
        f1_hash = f2_hash
        f3_hash = f4_hash
        file1 = open("x.txt", "r+")
        file2 = open("y.txt", "r+")
        if((os.stat("x.txt").st_size != 0)&(os.stat("y.txt").st_size != 0)):
            x = int(file1.read())
            y = int(file2.read())
            if count==0:
                cnc1(x, y)
                count=1
            else:
                count=0
        
        file1.close()
        file2.close()
