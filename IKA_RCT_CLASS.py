# Author:           Markus Kirchner
# Date:             2024-03-18
# Last modified:    2024-03-19
# Version:          0.2

from TCPIP_TO_RS232_DEVICE_CLASS import *

# The safety temperature limit must always be set to at least +25°C lower than the fire point of media used.

# The adjustable maximum heating plate temperature must always be set at least +15°C under the set safety temperature limit.

# Setting range: [+100°C] to [max. SET temperature +650°C]

# Each individual command (incl. parameters and data) and each response are terminated with Blank CR LF and have a maximum
# length of 80 characters.

IKA_RCT_HEATER = 5500
IKA_RCT_STIRRER = 5501

IKA_RCT_OPERATING_MODE_A = 9000 # After power on heater and stirrer remain off 
IKA_RCT_OPERATING_MODE_B = 9001 # After power on heater and stirrer are set to their previos state (on or off)
IKA_RCT_OPERATING_MODE_D = 9002

IKA_RCT_WATCHDOG_MODE_1 = 6000
IKA_RCT_WATCHDOG_MODE_2 = 6001

#self, host, port, buffer_size=1024, send_termination_character="\r\n", receive_termination_character="\r\n"

class IKA_RCT_CLASS (TCPIP_TO_RS232_DEVICE_CLASS):
    def __init__(self, host, port):
        super().__init__(host, port, 128, "\r\n","\r\n")
                
    def getDeviceName(self):
        if not self.connected: return "Error"
        self.send("IN_NAME")
        return(self.recv()) 
    
    def __setValue__(self, property,value):
        if not self.connected: return "Error"
        if type(property) == int: property = str(property)
        self.send("OUT_SP_%s %s" % (property ,str(value))) 

    def __read__(self, msg):
        if not self.connected: return "Error"
        self.send(msg)
        return self.recv()

    def __readPV__(self,property):
        if not self.connected: return "Error"
        if type(property) == int: property=str(property)
        tmpList = self.__read__("IN_PV_%s" % property).split(" ")
        return(float(tmpList[0])) 
    
    def __readSP__(self,property):
        if not self.connected: return "Error"
        if type(property) == int: property=str(property)
        tmpList = self.__read__("IN_SP_%s" % property).split(" ")
        return(float(tmpList[0])) 
    # RS232 commands (getters):
    def getExtSensorValue(self):
        if not self.connected: return "Error"
        return self.__readPV__(1)

    def getHotplateTemp(self):
        if not self.connected: return "Error"
        return self.__readPV__(2)
    
    def getCurrentStirringSpeed(self):
        if not self.connected: return "Error"     
        return(int(self.__readPV__(4))) 
    
    def getViscosityTrendValue(self):
        if not self.connected: return "Error"
        return float(self.__readPV__(5)) #not clear which kind of datatype is to be expected

    def getRatedTemperatureValue(self):
        if not self.connected: return "Error"
        return float(self.__readSP__(1))
    
    def getSafetyTemperatureValue(self):
        if not self.connected: return "Error"
        return float(self.__readSP__(3))
    
    def getRatedSpeedValue(self):
        if not self.connected: return "Error"
        return int(self.__readSP__(4))
    
    
    
    # RS232 commands (setters):

    def setRatedTemperature(self,temperature):
        if not self.connected: return "Error"
        if type(temperature) == int: temperature = float(temperature)
        if type(temperature) != float: return "Error"
        self.__setValue__(1,temperature)

    def setStirringSpeed(self,rpm):
        if not self.connected: return "Error"
        if type(rpm) != int: return "Error"
        self.__setValue__(4,rpm)

    def switchOn(self,Device=IKA_RCT_STIRRER):
        if not self.connected: return "Error"
        if Device == IKA_RCT_HEATER:
            self.send("START_1")
        elif Device == IKA_RCT_STIRRER:
            self.send("START_4")

    def switchOff(self,Device=IKA_RCT_STIRRER):
        if not self.connected: return "Error"
        if Device == IKA_RCT_HEATER:
            self.send("STOP_1")
        elif Device == IKA_RCT_STIRRER:
            self.send("STOP_4")

    def setOperationMode(self,mode=IKA_RCT_OPERATING_MODE_A):
        if not self.connected: return "Error"
        if type(mode) == int:
            command = "SET_MODE_"
            if mode == IKA_RCT_OPERATING_MODE_A:
                command = "%sA" % command
                self.send(command)
            elif mode == IKA_RCT_OPERATING_MODE_B:
                command = "%sB" % command
                self.send(command)
            elif mode == IKA_RCT_OPERATING_MODE_D:
                command = "%sD" % command
                self.send(command)

    def setWatchdogSafetyLimitTemperatureValue(self, temperature):
        if not self.connected: return "Error"
        if type(temperature) == int: temperature = float(temperature)
        if type(temperature) == float:
            self.send("OUT_SP_12@%1.1f" % temperature) # works with either "@" or " " between command and value
            return float(self.recv())
        return "Error"
    
    def setWatchdogSafetyLimitSpeedValue(self, speed):
        if not self.connected: return "Error"
        if type(speed) == float: speed = int(speed)
        if type(speed) == int:
            self.send("OUT_SP_42@%i" % speed) # works with either "@" or " " between command and value
            return float(self.recv())
        return "Error"
    


    # Remaining RS232 commands:
            
    def reset(self):
        if not self.connected: return "Error"
        self.send("RESET")

    def startWatchdog(self,mode,timeout):
        if not self.connected: return "Error"
        if type(mode) == int:
            if type(timeout) == int: timeout = float(timeout)
            if timeout:     # do not check boundarie values if timeout equals zero because zero is used to reset the watchdog
                if timeout <20: # Set to minumum value if passed value lies below minimum value
                    timeout = 20
                elif timeout > 1500: # Set to maximum value if passed value lies above maximum value
                    timeout = 1500
            if mode == IKA_RCT_WATCHDOG_MODE_1:
                self.send("OUT_WD1@%1.1f" % timeout) # works only with '@' instead of ' ' 
            elif mode == IKA_RCT_WATCHDOG_MODE_2:
                self.send("OUT_WD2@%1.1f" % timeout) # works only with '@' instead of ' ' 
            return float(self.recv())
    
    def resetWatchdog(self):
        if not self.connected: return "Error"
        return self.startWatchdog(IKA_RCT_WATCHDOG_MODE_2,0)




#Example/Test-cases:
    
if __name__ == "__main__":
    import time

    delay = 3

    objIKA = IKA_RCT_CLASS("192.168.178.50",23)
    objIKA.connect()
    print("Is connected: %s" % objIKA.connected)

    print("Device name: >%s<" % objIKA.getDeviceName())
    print("Hotplate temperature: %f" % objIKA.getHotplateTemp())
    print("External sensor value: %f" % objIKA.getExtSensorValue())
    print("Current stirring speed: %i " % objIKA.getCurrentStirringSpeed())
    print("Current viscosity trend value: %f%%" % objIKA.getViscosityTrendValue())
    print("Rated temperature value is: %f" % objIKA.getRatedTemperatureValue())
    print("Set safety temperature value is: %f" % objIKA.getSafetyTemperatureValue())
    print("Rated speed value is: %f" % objIKA.getRatedSpeedValue())
    objIKA.setRatedTemperature(120.7)
    objIKA.setStirringSpeed(115)

    objIKA.switchOn(IKA_RCT_HEATER)
    time.sleep(delay)
    objIKA.switchOff(IKA_RCT_HEATER)

    objIKA.switchOn(IKA_RCT_STIRRER)
    time.sleep(delay)
    print("Current viscosity trend value: %f%%"%objIKA.getViscosityTrendValue())
    objIKA.switchOff(IKA_RCT_STIRRER)

    objIKA.setOperationMode(IKA_RCT_OPERATING_MODE_B)
    time.sleep(delay)
    objIKA.setOperationMode(IKA_RCT_OPERATING_MODE_D)
    time.sleep(delay)
    objIKA.setOperationMode(IKA_RCT_OPERATING_MODE_A)
    print("Watchdog safety limit temperature value is set to %f" % objIKA.setWatchdogSafetyLimitTemperatureValue(50))
    print("Watchdog safety limit speed value is set to %i" % objIKA.setWatchdogSafetyLimitSpeedValue(40))


    #Test Watchdog mode 1:
    objIKA.switchOn(IKA_RCT_STIRRER)
    for i in range(2):
        print(objIKA.startWatchdog(IKA_RCT_WATCHDOG_MODE_1,20))
        time.sleep(15)
    time.sleep(10)
    print("Wathdog has been resetted; RCT returned: %s" % objIKA.resetWatchdog())

    #Test Watchdog mode 2:
    objIKA.switchOn(IKA_RCT_STIRRER)
    for i in range(2):
        print(objIKA.startWatchdog(IKA_RCT_WATCHDOG_MODE_2,20))
        time.sleep(15)
    time.sleep(10)
    print("Wathdog has been resetted; RCT returned: %s" % objIKA.resetWatchdog())
    time.sleep(1)
    objIKA.switchOff(IKA_RCT_STIRRER)
    time.sleep(5) #if connection will be closed before command could be executed, the command will never be executed!
    objIKA.close()
    print("Is connected: %s" % objIKA.connected)





        
        



