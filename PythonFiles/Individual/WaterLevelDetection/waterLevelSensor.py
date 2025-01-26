#import os
import Jetson.GPIO as GPIO
import time

GPIO.setwarnings(False)
##WaterLevelSensorPin = 18
GPIO.setmode(GPIO.BCM)
##GPIO.setup(WaterLevelSensorPin, GPIO.IN)

def Init_WaterLevelSensorPin(WaterLevelSensorPin):
    GPIO.setup(WaterLevelSensorPin, GPIO.IN)
    print("WaterLevelSensorPin initiated...")

def get_status_WaterLevelValue(WaterLevelSensorPin):
    time.sleep(0.2)
    val = GPIO.input(WaterLevelSensorPin)
    print("Current Water level is:", val)
    return val

def get_status_WaterLevel(WaterLevelSensorPin = 9):
    Init_WaterLevelSensorPin(WaterLevelSensorPin)
    time.sleep(0.2)
    
    if get_status_WaterLevelValue(WaterLevelSensorPin) == 1:
        
        print("Water level sufficient...")

    else:
        print("Water level not sufficient...")
        print("Make sure enough water is available in container...")

def reg_status_WaterLevel(WaterLevelSensorPin = 9, iterations = 10):
    Init_WaterLevelSensorPin(WaterLevelSensorPin)
    time.sleep(0.2)
    regValSum = 0
    for y in range(iterations):
        regVal = get_status_WaterLevelValue(WaterLevelSensorPin)
        regValSum =regValSum+regVal

    regValSum = regValSum/iterations
    print("RegValSum", regValSum)
    if regValSum > 0.7:
        print("Regression Water value accepted ")
    else :
        print("Regression Water value not accepted ")
    return regValSum
    

try:
    while True:
        #Value = reg_status_WaterLevel(WaterLevelSensorPin = 18, iterations = 10)
        #print("Regression Water level is", Value)
        get_status_WaterLevel(WaterLevelSensorPin = 18)
        time.sleep(0.2)

except keyboardInterrupt:
    GPIO.cleanup()

