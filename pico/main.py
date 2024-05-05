from machine import Pin, SPI, SoftSPI, UART, SoftI2C
from logs import *
from funcs import *
import time

# magic
true = True
false = False
# Function to initialize the sensors
def Initial():
    global Log
    global Sensor
    Log = log(SPI(1,baudrate=40000000,sck=Pin(10),mosi=Pin(11),miso=Pin(12)), #sd spi
              Pin(13), #sd sdp
              UART(0, baudrate=9600, tx=0, rx=1), #lora uart
              [Pin(2), Pin(3)], #lora m0, m1
              69 #Channel
              )
    Sensor = sensors(SoftI2C(sda=Pin(4), scl=Pin(5)), # i2c
                     Pin(6), #dht11 pin
                     UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9)), #gps uart
                     Log #Log
                     )


# Main loop
def Main():
    On = true
    while On:
        try:
            Log.DataLog(Sensor.GetSensorData())
            time.sleep(1)
            
            # Read Lora
            # if Log.ReadLora() != 0:
            #     Log.InfoLog("Receaved code: {}".format(Log.Code))
            #     if Log.Code == "end":
            #         Log.InfoLog("End")
            #         On = false
            #         break
            #     elif Log.Code == "reset":
            #         Initial()
            #         Log.InfoLog("Reset")
            #     else:
            #         Log.InfoLog("Unknown code")
                
            # End of the main loop
            time.sleep(0.2)
        except KeyboardInterrupt:
            On = false
            Log.InfoLog("Keyboard Interrupt")
            break
        except Exception as e:
             Log.ErrorLog("Fatal Error: {}".format(e))
# Initial function
Initial()
# Wait for 1 second
time.sleep(1)
Log.InfoLog("Starting")
# Main loop
Main()
Log.InfoLog("Ending")