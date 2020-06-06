"""
Python script to monitor HC-SR04 distance sensor for n seconds. 
"""


#Libraries
import argparse

class ultrasonic_measure:
    import RPi.GPIO as GPIO
    import time
    from datetime import datetime
    import os
     
    def distance(self):
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
     
    def save(self,filename, timestamp):
        basename = filename
        if timestamp: 
            folder = os.sep.join(filename.split(os.sep)[:-1])
            if not os.path.isdir(folder): 
                os.makedirs(folder)
            filen = datetime.today.strftime('%Y-%m-%d_%H-%M') + '_' + filename
            basename = os.sep.join(folder, filen)
        i = 1
        file_name_to_use = basename + '_' + str(i) + '.log'
        while os.path.isfile(file_name_to_use):
            i += 1
            file_name_to_use = basename + '_' + str(i) + '.log'
            
        with open(file_name_to_use,'w') as fil: 
            fil.write('Distance,UnderThreshold,Timestamp\n')
            for dataline in self.data: 
                fil.write(','.join([str(x) for x in dataline])+'\n')
            self.data = []
                
    def measure(self,duration, threshold):
        data = []
        for i in args.duration: 
            StartTime = time.time()
            dist = distance()
            threshpass = (dist < args.threshold)
            data.append([dist, threshpass, datetime.now().strftime('%H:%M:%S')])
            while (time.time()-dist) < 1:
                pass
        self.data = data
        
    def __init__(self,trigpin=18,echopin=24,mode=GPIO.BCM):
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(mode)
         
        #set GPIO Pins
        GPIO_TRIGGER = trigpin
        GPIO_ECHO = echopin
         
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        self.data = []
    
 
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('duration', type=int, help='Number of seconds to take measurements for. Measurements will be taken once per second.')
    parser.add_argument('output_name', help='Path and name for the output file without file extension. If file exists, a new file with _1, _2 etc will be created as needed. If directory the file is in does not exist, it will be created.')
    parser.add_argument('-t','--threshold',type=int,default=50,help='Add a filter column to output with True, if distance is lower than this threshold.')
    parser.add_argument('-ts','--timestamp',action='store_true',help='Prepend time stamp to output file.')
    args = parser.parse_args()
    
    measurer = ultrasonic_measure()
    measurer.measure(args.duration, args.threshold)
    measurer.save(args.output_name, args.timestamp)
    GPIO.cleanup()
    sys.exit()