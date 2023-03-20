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
cube = 41
half_cube=42/2
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(21, GPIO.OUT)           # set GPIO24 as an output   

p_count=0
p_arry=[9.5,9,8.5,8,19.5,19,18.5,18]

P_count=0
P_arry=[49.5,49,48.5,48,59.5,59,58.5,58]

r_count=0
r_arry=[39.5,39]

R_count=0
R_arry=[79.5,79]

n_count=0
n_arry=[29.5,29]

N_count=0
N_arry=[69.5,69]

b_count=0
b_arry=[28.5,28]

B_count=0
B_arry=[68.5,68]

q_arry=38.5
Q_arry=78.5
k_arry=79
K_arry=79.5

import heapq
import chess
import numpy as np

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(array, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

def filter_points(points):
    filtered_points = [points[0]]
    for i in range(1, len(points) - 1):
        if (points[i][0] == points[i - 1][0] and points[i][0] == points[i + 1][0]) or (points[i][1] == points[i - 1][1] and points[i][1] == points[i + 1][1]) or (abs(points[i][0] - points[i - 1][0]) == abs(points[i][1] - points[i - 1][1]) and abs(points[i][0] - points[i + 1][0]) == abs(points[i][1] - points[i + 1][1])):
            continue
        filtered_points.append(points[i])
    filtered_points.append(points[-1])
    return filtered_points


def filter_points_V2(points):
    filtered_points = []
    for i in range(1, len(points) - 1):
        if (points[i][0] == points[i - 1][0] and points[i][0] == points[i + 1][0]) or (points[i][1] == points[i - 1][1] and points[i][1] == points[i + 1][1]) or (abs(points[i][0] - points[i - 1][0]) == abs(points[i][1] - points[i - 1][1]) and abs(points[i][0] - points[i + 1][0]) == abs(points[i][1] - points[i + 1][1])):
            continue
        filtered_points.append(points[i])
    filtered_points.append(points[-1])
    if (points[0][0] == points[1][0] and points[0][0] == points[2][0]) or (points[0][1] == points[1][1] and points[0][1] == points[2][1]) or (abs(points[0][0] - points[1][0]) == abs(points[0][1] - points[1][1]) and abs(points[0][0] - points[2][0]) == abs(points[0][1] - points[2][1])):
        return filtered_points
    else:
        return [points[0]]+filtered_points
def make_matrix(board): #type(board) == chess.Board()
    pgn = board.epd()
    foo = []  #Final board
    pieces = pgn.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  #This is the row I make
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('0')
            else:
                foo2.append(thing)
        foo.append(foo2)
    foo.reverse()
    return foo

def write_read(num):
    arduino.write("\r\n\r\n".encode('utf-8')+num.encode('utf-8')+"\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data
def write_read2(num):
    arduino.write("\r\n\r\n".encode('utf-8')+num.encode('utf-8')+"\r\n\r\n".encode('utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    arduino.flushInput()
    arduino.write("?".encode('utf-8'))
    data2 = arduino.readline()
    after_decode=data2.decode('utf-8')
    while (after_decode[1:4]=="Jog"):
        arduino.flushInput()
        arduino.write("?".encode('utf-8'))
        data2 = arduino.readline()
        after_decode=data2.decode('utf-8')
    time.sleep(0.25)
    return data
def alphabetical_value(str):
    return 'abcdefghijklmnopqrstuvwxyz'.index(str.lower()) + 1

def cnc1(x,y):
    led.on()
    XSUM = 0
    YSUM = 0
    cube = 41
    half_cube=42/2
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
    
    arduino.flushInput()

    
    GPIO.output(21, 0)
    
    
    
    file1 = open('location.txt', 'r')
    Lines = file1.read()
    
 
    
    XSTART = x % 8
    YSTART = x // 8
    XEND=y%8
    YEND=y//8
    
    board = chess.Board(Lines)
    arr = np.array(make_matrix(board))
    print(arr)
    mask = np.zeros_like(8)
    mask = arr !='0'
    mask=mask*1
    mask[YSTART][XSTART]=0
    mask[YEND][XEND]=0
    # start position
    start = (YSTART,XSTART)
    print(start)
    # end position
    end = (YEND,XEND)
    print(end)
    
    chess_board = mask.tolist()
    chess_board = np.array(chess_board)
    print(chess_board)
    path = astar(chess_board, start, end)
    print(path)
    if path:
        new_path=path
        new_path.reverse()
        print(new_path)
        if(len(new_path)==1):
            num = '$J=G21G91X' + str(cube*(XSTART)) + 'Y' + str(cube*YSTART) + 'F10000'
            print(num)
            value = write_read2(num)
            print(value.decode('utf-8'))
            XSUM+= cube*(XSTART)
            YSUM+= cube*YSTART
            GPIO.output(21, 1)#enbale electro
            num = '$J=G21G91X' + str(cube*(XEND-XSTART)) + 'Y' + str(cube*(YEND-YSTART)) + 'F10000'
            print(num)
            value = write_read2(num)
            print(value.decode('utf-8'))
            XSUM+= cube*(XEND-XSTART)
            YSUM+= cube*(YEND-YSTART)
        if(len(new_path)>=2):
            if(len(new_path)==2):
                new_path.insert(0,(YSTART,XSTART))
            fliterd=filter_points_V2(new_path)
            print(fliterd)
            num = '$J=G21G91X' + str(cube*(XSTART)) + 'Y' + str(cube*(YSTART)) + 'F10000'
            print(num)
            value = write_read2(num)
            print(value.decode('utf-8'))
            XSUM+= cube*(XSTART)
            YSUM+= cube*(YSTART)
            GPIO.output(21, 1)#enbale electro
            
            num = '$J=G21G91X' + str(cube*(fliterd[0][1]-XSTART)) + 'Y' + str(cube*(fliterd[0][0]-YSTART)) + 'F10000'
            print(num)
            value = write_read2(num)
            print(value.decode('utf-8'))
            XSUM+= cube*(fliterd[0][1]-XSTART)
            YSUM+= cube*(fliterd[0][0]-YSTART)
            for i in range(len(fliterd)-1):
                print(fliterd[i])
                num = '$J=G21G91X' + str(cube*(fliterd[i+1][1]-fliterd[i+0][1])) + 'Y' + str(cube*(fliterd[i+1][0]-fliterd[i+0][0])) + 'F10000'
                print(num)
                value = write_read2(num)
                print(value.decode('utf-8'))
                XSUM+= cube*(fliterd[i+1][1]-fliterd[i+0][1])
                YSUM+= cube*(fliterd[i+1][0]-fliterd[i+0][0])
        GPIO.output(21, 0)#disable electro
        num = '$J=G21G91X' + str(-XSUM) + 'Y' + str(-YSUM) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))
        XSUM=0
        YSUM=0
        
    else:
        Xstep=cube*(XSTART)
        Ystep=cube*(YSTART)
        XSUM+= Xstep
        YSUM+= Ystep
        print("Y STEP VALUE",Ystep)
        #A2TOB3
        num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))
        
        GPIO.output(21, 1)#enbale electro
        XSUM+= half_cube
        num = '$J=G21G91X' + str(half_cube) + 'Y' + str(0) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))

        
        Xstep=0
        Ystep=cube*(YEND-YSTART)-half_cube
        flip=1
        if(Ystep<0):
            Ystep=Ystep+42
            flip=-1
        YSUM+= Ystep
        num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))

        
        Ystep=0
        Xstep=cube*(XEND-XSTART)
        XSUM+= Xstep
        num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))

        XSUM_temp=XSUM
        x_move=-half_cube-5
        y_move=flip*(half_cube+5)
        XSUM+=-half_cube-5
        YSUM+= flip*(half_cube+5)
        if(XEND==0):
            x_move=x_move+5
            y_move=y_move+5
            XSUM+=5
            YSUM+=5
        num = '$J=G21G91X' + str(x_move) + 'Y' + str(y_move) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))

        
        GPIO.output(21, 0)#disable electro
        """
        Xstep=cube*(XEND-XSTART)
        Ystep=0
        XSUM+= Xstep
        num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))
        """

        num = '$J=G21G91X' + str(-XSUM) + 'Y' + str(-YSUM) + 'F10000'
        print(num)
        value = write_read2(num)
        print(value.decode('utf-8'))

        XSUM=0
        YSUM=0
        print("finish move")
        led.off()
        return


def cnc_remove(x,y):
    led.on()
    print("This X "+ str(x))
    print("This Y "+ str(y))
    XSUM = 0
    YSUM = 0
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
    XEND=y%10
    YEND=y//10 +y%0.5
    
    Xstep=cube*(XSTART)
    Ystep=cube*(YSTART)
    XSUM+= Xstep
    YSUM+= Ystep
    print("Y STEP VALUE",Ystep)
    #A2TOB3
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    value = write_read2(num)
    print(value.decode('utf-8'))

    
    GPIO.output(21, 1)#enbale electro
    XSUM+= half_cube
    num = '$J=G21G91X' + str(half_cube) + 'Y' + str(0) + 'F10000'
    print(num)
    value = write_read2(num)
    print(value.decode('utf-8'))

    
    Xstep=0
    Ystep=cube*(YEND-YSTART)+half_cube
    print(YEND)
    print(YSTART)
    print(YEND-YSTART)
    YSUM+= Ystep
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    value = write_read2(num)
    print(value.decode('utf-8'))

    
    Ystep=0
    Xstep=cube*(XEND-XSTART-1)
    XSUM+= Xstep
    num = '$J=G21G91X' + str(Xstep) + 'Y' + str(Ystep) + 'F10000'
    print(num)
    value = write_read2(num)
    print(value.decode('utf-8'))
    
    YSUM=YSUM-half_cube
    num = '$J=G21G91X' + str(0) + 'Y' + str(-half_cube) + 'F10000'
    print(num)
    value = write_read2(num)
    print(value.decode('utf-8'))
    
    GPIO.output(21, 0)#disable electro

    num = '$J=G21G91X' + str(-XSUM) + 'Y' + str(-YSUM) + 'F10000'
    print(num)
    value = write_read2(num)
    print(value.decode('utf-8'))
    XSUM=0
    YSUM=0
    led.off()
    print("finish remove")
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

count_temp=0
# Calling hashfile() function to obtain hashes
# of the files, and saving the result
# in a variable

f_remove_hash_1 = hashfile("remove.txt")
f1_hash = hashfile("x.txt")
f3_hash = hashfile("y.txt")

while True:
    f_remove_hash_2 = hashfile("remove.txt")
    f2_hash = hashfile("x.txt")
    f4_hash = hashfile("y.txt")
    x_temp=0
    y_temp=0
    # Doing primitive string comparison to
    # check whether the two hashes match or not
    if (f_remove_hash_1 == f_remove_hash_2):
        None
    else:
        print("Files are different!")
        print(f"Hash of File 1_remove: {f1_hash}")
        print(f"Hash of File 2_remove: {f2_hash}")
        f_remove_hash_1 = f_remove_hash_2
        f1_hash = f2_hash
        f3_hash = f4_hash
        time.sleep(0.25)
        file_remove = open("remove.txt", "r+")
        time.sleep(0.25)
        file1 = open("x.txt", "r+")
        time.sleep(0.25)
        file2 = open("y.txt", "r+")
        
        if((os.stat("x.txt").st_size != 0) & (os.stat("y.txt").st_size != 0)&(os.stat("remove.txt").st_size != 0)):
            name_of_piece = file_remove.read()
            time.sleep(0.25)
            x = int(file1.read())
            time.sleep(0.25)
            y = int(file2.read())
            
            #print("THE COUNTTTTTT ",count_temp)
            #if(count_temp>1):
              #  count_temp=0
               # break
            #count_temp+=1
            if count<1:
                count+=1
                continue
            else:
                count=0
                
            if name_of_piece=='p':
                cnc_remove(y, float(p_arry[p_count]))
                p_count+=1
                cnc1(x,y)

            if name_of_piece=='P':
                cnc_remove(y, float(P_arry[P_count]))
                P_count+=1
                cnc1(x,y)
                
            if name_of_piece=='r':
                cnc_remove(y, float(r_arry[r_count]))
                r_count+=1
                cnc1(x,y)
                
            if name_of_piece=='R':
                cnc_remove(y, float(R_arry[R_count]))
                R_count+=1
                cnc1(x,y)
                
            if name_of_piece=='n':
                cnc_remove(y, float(n_arry[n_count]))
                n_count+=1
                cnc1(x,y)
                
            if name_of_piece=='N':
                cnc_remove(y, float(N_arry[N_count]))
                N_count+=1
                cnc1(x,y)
                
            if name_of_piece=='b':
                cnc_remove(y, float(b_arry[b_count]))
                b_count+=1
                cnc1(x,y)
                
            if name_of_piece=='B':
                cnc_remove(y, float(B_arry[B_count]))
                B_count+=1
                cnc1(x,y)
                
            if name_of_piece=='q':
                cnc_remove(y, float(q_arry))
                cnc1(x,y)
                
            if name_of_piece=='Q':
                cnc_remove(y, float(Q_arry))
                cnc1(x,y)
                
            if name_of_piece=='k':
                cnc_remove(y, float(k_arry))
                cnc1(x,y)
                
            if name_of_piece=='K':
                cnc_remove(y, float(K_arry))
                cnc1(x,y)
                
            file1.close()
            file2.close()
            file_remove.close()
    
    if (f1_hash == f2_hash) and (f3_hash == f4_hash):
        continue
    else:
        print("Files are different!")
        print(f"Hash of File 1: {f1_hash}")
        print(f"Hash of File 2: {f2_hash}")
        f_remove_hash_1 = f_remove_hash_2
        f1_hash = f2_hash
        f3_hash = f4_hash
        time.sleep(0.25)
        file1 = open("x.txt", "r+")
        time.sleep(0.25)
        file2 = open("y.txt", "r+")
        if((os.stat("x.txt").st_size != 0)&(os.stat("y.txt").st_size != 0)):
            time.sleep(0.25)
            x = int(file1.read())
            time.sleep(0.25)
            y = int(file2.read())
            if count==0:
                cnc1(x, y)
                count=1
            else:
                count=0
        
        file1.close()
        file2.close()
    



