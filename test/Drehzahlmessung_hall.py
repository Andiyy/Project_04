import RPi.GPIO as GPIO
import time

HallPin = 11
Zähler = 0

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(HallPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.add_event_detect(HallPin, GPIO.FALLING, callback=detect, bouncetime=25)
    
def Print(x):
    global Zähler
    if x == 0:
        Zähler += 1
        print(Zähler)
        print ('    ***********************************')
        print ('    *   Detected magnetic materials   *')
        print ('    ***********************************')

def detect(chn):
    Print(GPIO.input(HallPin))
    pass
'''
v = d x pi x n oder v = w * r 
'''
    
def loop():
    while True:
        if GPIO.event_detected(HallPin):
            # time.sleep(0.01)
            pass

def destroy():
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()