import random

from fastapi import FastAPI
from pydantic import BaseModel

class Sensor(BaseModel):
    sensor_name = ''
    sensor_data : float = 0.0

    def init(self):
        return self
    
    def getData(self):
        self.sensor_data = round(random.uniform(0,100), 2)

sensor1 = Sensor(sensor_name='T1').init()

application = FastAPI()

@application.get("/get-data", response_model=Sensor)
def get_data():
    sensor1.getData()
    return sensor1
