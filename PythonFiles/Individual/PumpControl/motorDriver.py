#import os
import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
## d24(18) enable, d23(16) input1,  d25(22) input2
GPIO.setmode(GPIO.BCM)


def Init_motorDriverPin(EnableA, Input1, Input2):
    GPIO.setup(EnableA, GPIO.OUT)
    GPIO.setup(Input1, GPIO.OUT)
    GPIO.setup(Input2, GPIO.OUT)
    print("EnableA, Input1, Input2 pins are initiated...")

def set_motor_on(EnableA, Input1, Input2):
    GPIO.output(EnableA, 1)
    GPIO.output(Input1, 1)
    GPIO.output(Input2, 0)
    print("Setting pump on")
def set_motor_off(EnableA, Input1, Input2):
    time.sleep(0.2)
    GPIO.output(EnableA, 1)
    GPIO.output(Input1, 0)
    GPIO.output(Input2, 0)
    print("Setting pump off")


Init_motorDriverPin(EnableA=24, Input1=23, Input2=22)
try:
    while True:
        set_motor_Forward(EnableA=24, Input1=23, Input2=22)
        print("while")
        time.sleep(0.7)
        set_motor_off(EnableA=24, Input1=23, Input2=22)

except keyboardInterrupt:
    GPIO.cleanup()

