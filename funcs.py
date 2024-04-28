import time
import machine
from mpu6050 import init_mpu6050, get_mpu6050_data
import math
from logs import *


class sensors:
    def __init__(self, mpu, dht, bmp):
        self.mpu = mpu
        try:
            init_mpu6050(self.mpu)
        except Exception as e:
            ErrorLog(e)
    
    def RawData(self):
        try:
            return get_mpu6050_data(self.mpu)
        except Exception as e:
            ErrorLog(e)
            return 0
    def Accel(self):
        try:
            data = get_mpu6050_data(self.mpu)['accel']
            data['x'] = round(data['x']-0.03, 1)
            data['y'] = round(data['y']-0.02, 1)
            data['z'] = round(data['z']+0.20, 1)
            return data
        except Exception as e:
            ErrorLog(e)
            return 0
    
    def Tilt(self):
        try:
            accel_data = self.Accel()
            if accel_data != 0:
                x, y, z = accel_data['x'], accel_data['y'], accel_data['z']
                pitch=math.atan(y/z)
                roll=math.atan(x/z)
                pitchDeg=round(pitch/(2*math.pi)*360)
                rollDeg=round(roll/(2*math.pi)*360)
                if rollDeg<0:
                    rollDeg+=180
                if x<0:
                    rollDeg+=180
                if z<0 and rollDeg == 0:
                    rollDeg = 180
                
                return round(pitchDeg), round(rollDeg)
            else:
                return (0, 0)
        except Exception as e:
            return (0, 90)

def GetTime():
    current_time = time.localtime()
    formatted_time = "{:02d}-{:02d}-{:02d}".format(current_time[3], current_time[4], current_time[5])
    return formatted_time