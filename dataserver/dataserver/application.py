from time import time
import random

from fastapi import FastAPI
from pydantic import BaseModel

class Sensor(BaseModel):
    sensor_name_list : list = []
    sensor_dict : dict ={}

    def init(self):
        for key in self.sensor_name_list:
            self.sensor_dict[key] = 0.0
        return self
    
    def getData(self):
        self.sensor_dict['time'] = time()
        for key in self.sensor_name_list:
            self.sensor_dict[key] = round(random.uniform(0,100), 2)

sensor_list = ['T1', 'T2', 'T3', 'T4', 'P1', 'P2', 'Pos']
sensor1 = Sensor(sensor_name_list=sensor_list).init()

application = FastAPI()

@application.get("/get-data", response_model=Sensor)
def get_data():
    sensor1.getData()
    return sensor1
