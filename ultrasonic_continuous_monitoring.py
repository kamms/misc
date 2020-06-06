"""
Continuously monitors a HC-SR04 distance sensor. 
"""

#Libraries
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import sys

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
def save(distances):
    basename = os.path.join(os.sep+'home', 'pi','distance_sensor',datetime.today().strftime('%Y-%m-%d_%H-%M'))
    i = 1
    file_name_to_use = basename + '_' + str(i) + '.log'
    while os.path.isfile(file_name_to_use):
        i += 1
        file_name_to_use = basename + '_' + str(i) + '.log'
        
    with open(file_name_to_use,'w') as fil: 
        fil.write('Distance,UnderThreshold,Timestamp\n')
        for col in collected: 
            fil.write(','.join([str(x) for x in col])+'\n')

 
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        threshold = int(sys.argv[1])
        saveinterval = int(sys.argv[2])
    else: 
        threshold = 40
        saveinterval = 15
    print(f'Using threshold: {threshold} and saving every {saveinterval} minutes')
    lastsave = datetime.now()
    try:
        collected = []
        while True:
            dist = distance()
            #print(dist)
            threshpass = (dist < threshold)
            collected.append([dist, threshpass, datetime.now().strftime('%H:%M:%S')])
            if threshpass: 
                time.sleep(1)
            else: 
                if (datetime.now()-lastsave).seconds >= (saveinterval*60):
                    lastsave = datetime.now()
                    save(collected)
                    collected = []
                time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        sys.exit()
