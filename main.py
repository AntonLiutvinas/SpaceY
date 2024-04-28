from machine import Pin, SPI, SoftSPI, UART, SoftI2C
from logs import *
from funcs import *
import time

def Initial():
    global Log
    global Sensor
    Log = log(SoftSPI(1, sck=Pin(14), mosi=Pin(12), miso=Pin(13)), #sd spi
              Pin(27), #sd sdp
              UART(2, baudrate=9600, tx=17, rx=16), #lora uart
              [Pin(2), Pin(15)], #lora m0, m1
              69 #Channel
              )
    Sensor = sensors(SoftI2C(sda=Pin(21), scl=Pin(22)), # mpu6050 i2c
                     0,
                     0
                     )
        
def Main():
    while True:
        print(Sensor.Tilt())
        time.sleep(0.2)
    
Initial()
Main()
