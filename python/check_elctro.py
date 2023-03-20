import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(21, GPIO.OUT)           # set GPIO24 as an output   
  
try:  
    while True:  
        GPIO.output(21, 1)         # set GPIO24 to 1/GPIO.HIGH/True
        print("press")
        sleep(5)                 # wait half a second  
        GPIO.output(21, 0)         # set GPIO24 to 0/GPIO.LOW/False
        print("relese")
        sleep(2)                 # wait half a second  
  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program 