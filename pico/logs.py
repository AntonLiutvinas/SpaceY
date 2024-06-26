import sdcard
import os
from funcs import *
from lora_e220 import LoRaE220, Configuration
import urandom

class log:
    def InitSd(self):
        try:
            sd=sdcard.SDCard(self.spi, self.sdp)
            vfs=os.VfsFat(sd)
            os.mount(sd,'/sd')
            self.FILE = "Logs-({}).txt".format(len(os.listdir('/sd')))
            file = open("/sd/{}".format(self.FILE),"w")
            file.close()
            return 1
        except Exception as e:
            return e
    
    def InitLora(self):
        try:
            LORA = LoRaE220('400T22D', self.lora, m0_pin=self.loraConfig[0], m1_pin=self.loraConfig[1])
            LORA.begin()
            configuration_to_set = Configuration('400T22D')
            configuration_to_set.CHAN = self.channel
            LORA.set_configuration(configuration_to_set)
            return 1
        except Exception as e:
            return e

    def __init__(self, spi, sdp, loraUart, loraConfig, channel):
        self.FILE = "Logs-{}.txt".format(str(urandom.randint(0, 10000000)))
        self.spi = spi
        self.sdp = sdp
        self.lora = loraUart
        self.loraConfig = loraConfig
        self.channel = channel
        self.Code = 0
        i = 0
        code = 0
        while i < 3:
            i+=1
            code = self.InitSd()
            if code == 1:
                break
            else:
                self.ErrorLog(code)
        i = 0
        code = 0
        while i < 3:
            i+=1
            code = self.InitLora()
            if code == 1:
                break
            else:
                self.ErrorLog(code)

    def Error(self, e):
        return "{tim}|e|{er}".format(tim=GetTime(), er=e)

    def Info(self, msg):
        return "{tim}|i|{ms}".format(tim=GetTime(), ms=msg)
    
    def Data(self, msg):
        return "{tim}|d|{ms}".format(tim=GetTime(), ms=msg)
    
    def InfoLog(self, msg):
        msg = self.Info(msg)
        self.WriteSd(msg)
        self.WriteLora(msg)
        print(msg)
    
    def DataLog(self, msg):
        msg = self.Data(msg)
        self.WriteSd(msg)
        self.WriteLora(msg)
        print(msg)

    def ErrorLog(self, msg):
        msg = self.Error(msg)
        try:
            file = open("/sd/{}".format(self.FILE),"a")
            file.write("{tim}|d|{ms}\n".format(tim=GetTime(), ms=msg))
            file.close()
        except Exception:
            pass
        try:
            self.lora.write('{:04d}'.format(len(msg)).encode())
            self.lora.write(msg.encode())
        except Exception:
            pass
        try:
            print(msg)
        except Exception:
            pass

    def WriteSd(self, msg):
        try:
            file = open("/sd/{}".format(self.FILE),"a")
            file.write("{}\n".format(msg))
            file.close()
            return 1
        except Exception as e:
            self.ErrorLog(e)
            return 0
    
    def ReadSd(self):
        try:
            file = open("/sd/{}".format(self.FILE),"r")
            msg = file.read()
            file.close()
            return msg
        except Exception as e:
            self.ErrorLog(e)
            return 0
        
    def WriteLora(self, msg):
        try:
            self.lora.write('{:04d}'.format(len(msg)).encode())
            self.lora.write(msg.encode())
            return 1
        except Exception as e:
            self.ErrorLog(e)
            return 0
    
    def ReadLora(self):
        try:
            length = self.lora.read(4)
            if length != None:
                self.Code = self.lora.read(int(length.decode())).decode()
                return 1
            return 0
        except Exception as e:
            self.ErrorLog(e)
            return 0

