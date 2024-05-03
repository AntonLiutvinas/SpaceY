from machine import Pin, SPI, SoftSPI, UART, SoftI2C
from logs import *
from funcs import *
import time

def Initial():
    global Log
    global Sensor
    Log = log(SoftSPI(1, sck=Pin(10), mosi=Pin(11), miso=Pin(12)), #sd spi
              Pin(13), #sd sdp
              UART(1, baudrate=9600, tx=17, rx=16), #lora uart
              [Pin(2), Pin(15)], #lora m0, m1
              69 #Channel
              )
    Sensor = sensors(SoftI2C(sda=Pin(21), scl=Pin(22)), # i2c
                     Pin(4), #dht11 pin
                     UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)), #gps uart
                     Log #Log
                     )
        
def Main():
    while True:
        print(Sensor.Tilt())
        time.sleep(0.2)
    
Initial()
Main()
