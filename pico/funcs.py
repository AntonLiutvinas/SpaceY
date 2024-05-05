import time
import machine
from mpu6050 import init_mpu6050, get_mpu6050_data
import math
import dht
from bmp280 import *

class sensors:
    def __init__(self, i2c, dht11, gps, Log):
        self.i2c = i2c
        self.Log = Log
        try:
            init_mpu6050(self.i2c)
        except Exception as e:
            Log.ErrorLog(e)
        try:
            self.dht11 = dht.DHT11(dht11)
        except Exception as e:
            Log.ErrorLog(e)
        try:
            self.bmp = BMP280(i2c)
        except Exception as e:
            self.Log.ErrorLog(e)
        try:
            self.gps = gps
        except Exception as e:
            self.Log.ErrorLog(e)

    def GetSensorData(self):
        try:
            # pr:pressure, al:altitude, te:temperature, hu:humidity, la:latitude, lo:longitude, sa:satellites, pi:pitch, ro:roll
            bmp_data = self.GetBmp()
            bio_data = self.GetBio()
            position_data = self.GetPositionData()
            tilt_data = self.Tilt()

            return f"pr:{bmp_data[0]},al:{bmp_data[1]},te:{bio_data[0]},hu:{bio_data[1]},la:{position_data[0]},lo:{position_data[1]},sa:{position_data[2]},pi:{tilt_data[0]},ro:{tilt_data[1]}"
        except Exception as e:
            self.Log.ErrorLog(e)
            return "pr:e,al:e,te:e,hu:e,la:e,lo:e,sa:e,pi:e,ro:e"

    def GetPositionData(self):
        timeout = time.time() + 8   # 8 seconds from now
        try:
            while True:
                self.gps.readline()
                buff = str(self.gps.readline())
                parts = buff.split(',')
                if (parts[0] == "b'$GPGGA" and len(parts) == 15):
                    if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                        latitude = self.convertToDigree(parts[2])
                        if (parts[3] == 'S'):
                            latitude = -latitude
                        longitude = self.convertToDigree(parts[4])
                        if (parts[5] == 'W'):
                            longitude = -longitude
                        satellites = parts[7]
                        return (latitude, longitude, satellites)
                if (time.time() > timeout):
                    return ("e", "e", "e")
        except Exception as e:
            self.Log.ErrorLog(e)
            return ("e", "e", "e")
        
    def convertToDigree(self, RawDegrees):
        try:
            RawAsFloat = float(RawDegrees)
            firstdigits = int(RawAsFloat/100) #degrees
            nexttwodigits = RawAsFloat - float(firstdigits*100) #minutes

            Converted = float(firstdigits + nexttwodigits/60.0)
            Converted = '{0:.6f}'.format(Converted) # to 6 decimal places
            return str(Converted)
        except Exception as e:
            self.Log.ErrorLog(e)
            return "e"

    def GetBmp(self):
        try:
            self.bmp.normal_measure()
            pressure = self.bmp.pressure
            pressure /= 100
            altitude = 44330 * (1.0 - (pressure / 1013.25) ** 0.1903)
            return (pressure, altitude)
        except Exception as e:
            self.Log.ErrorLog(e)
            return ("e", "e")

    def GetBio(self):
        try:
            self.dht11.measure()
            return (self.dht11.temperature(), self.dht11.humidity())
        except Exception as e:
            self.Log.ErrorLog(e)
            return ("e", "e")

    def RawDataG(self):
        try:
            return get_mpu6050_data(self.mpu)
        except Exception as e:
            self.Log.ErrorLog(e)
            return 0
        
    def Accel(self):
        try:
            data = get_mpu6050_data(self.mpu)['accel']
            data['x'] = round(data['x']-0.03, 1)
            data['y'] = round(data['y']-0.02, 1)
            data['z'] = round(data['z']+0.20, 1)
            return data
        except Exception as e:
            self.Log.ErrorLog(e)
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