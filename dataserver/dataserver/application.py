from time import time, sleep
import random

from fastapi import FastAPI
from pydantic import BaseModel
import RPi.GPIO as GPIO

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
    sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time()
    StopTime = time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time()
        if StartTime -StopTime > 1:
            return 0.0


    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time()
        if StopTime - StartTime > 1:
            return 0.0


    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

class Sensor(BaseModel):
    sensor_name_list : list = []
    sensor_dict : dict ={}

    def init(self):
        for key in self.sensor_name_list:
            self.sensor_dict[key] = 0.0
        return self

    def getData(self):
        self.sensor_dict['time'] = time()
        dist = round(distance(),1)
        for key in self.sensor_name_list:
            if key == 'P1' or key == 'P2':
                self.sensor_dict[key] = dist
            else:
                self.sensor_dict[key] = round(random.uniform(0,100), 2)

sensor_list = ['T1', 'T2', 'T3', 'T4', 'P1', 'P2', 'Pos']
sensor1 = Sensor(sensor_name_list=sensor_list).init()

application = FastAPI()

@application.get("/get-data", response_model=Sensor)
def get_data():
    sensor1.getData()
    return sensor1
