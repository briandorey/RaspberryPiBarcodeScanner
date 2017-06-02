#!/usr/bin/env python3

from lib import LTC2943_1
import subprocess
import time
import serial
import os

import subprocess as s

class Hardware:
    """All functions related to accessing the barcode scanner hardware"""

    __MINVOLTAGE = 6.4
    __MAXVOLTAGE = 8.0

    Port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1.0)
    

    ##### Private GPIO Functions #####

    def __read_gpio(self, pin) :
        process = s.Popen(["/usr/local/bin/gpio", "read", pin], stdout = s.PIPE)
        data, _ = process.communicate()
        datastr = data.decode("utf-8")
        datastr = str.replace(datastr, "\r", "")
        datastr = str.replace(datastr, "\n", "")

        return datastr

    def __write_gpio(self, pin, status) :
        process = s.Popen(["/usr/local/bin/gpio", "write", pin, status], stdout = s.PIPE)
        stdout, stderr = process.communicate()

    def __gpio_mode(self, pin, mode) :
        process = s.Popen(["/usr/local/bin/gpio", "mode", pin, mode], stdout = s.PIPE)
        stdout, stderr = process.communicate()

    ##### Public Functions #####

    def init_battery_monitor(self):
        #
        # initialise the LTC2943_1 battery monitor IC
        #

        dev = LTC2943_1.LTC2943_1()
        dev.set_control(0xC0) #ADC = Automatic Mode | Prescaler = 1 | ALCC = Disabled | Shutdown = no
        dev.set_charge_threshold_high(0xFFFF)
        dev.set_charge_threshold_low(0x0000)
        dev.set_voltage_threshold_high(0xFFFF)
        dev.set_voltage_threshold_low(0x0000)
        dev.set_current_threshold_high(0xFFFF)
        dev.set_current_threshold_low(0x0000)
        dev.set_temperature_threshold_high(0xFF)
        dev.set_temperature_threshold_low(0x00)

        return (1)

    def get_battery_level(self):
        #
        # Get the battery level from the LTC2943
        #
        dev = LTC2943_1.LTC2943_1()
        data = dev.get_data()

        batteryvoltage = dev.parse_voltage(data)

        batterylevel = (batteryvoltage - self.__MINVOLTAGE) * 100
        if batterylevel < 0:
            batterylevel = 0
        if batterylevel > 100:
            batterylevel = 100
        
        return (str(int(batterylevel)))

    def get_wifi_strength(self):
        #
        # get the signal strength from the current wifi connection using iwconfig
        #

        bashCommand = "iwconfig wlan0 | grep Quality"
        wifibytes = subprocess.check_output(['bash','-c', bashCommand])
        wifistr = wifibytes.decode("utf-8")
        strengthlocation = wifistr.find("=")
        signalstrength = str(wifistr)[strengthlocation + 1:strengthlocation + 4].replace("/", "")
        
        return (str(signalstrength))

    def init_scanner(self):
        #
        # Initialise the GPIO and UART for scanning
        #

        # set the direction of the GPIO pins and clear the receive buffer on the uart port
        self.__gpio_mode("3","out")
        self.__gpio_mode("4","in")
        self.__write_gpio("3", "1")
        self.Port.flushInput()

    def scan(self):
        #
        # Call the scanner and read the serial buffer
        #
        
        #­ flush the input buffer
        self.Port.flushInput()
    
        # enable barcode scanner on GPIO 22
        self.__write_gpio("3", "0")

        ScanTimeout = time.time() + 5   # 5 seconds from now
        CodeFound = 0

        while True:
            if self.__read_gpio("4") == "1":
                CodeFound = 1
                break

            if time.time() > ScanTimeout:        
                break

        self.__write_gpio("3", "1")

        if CodeFound == 1:
            try:
                State = self.Port.read(13)
                return (State.decode("utf-8"))
            except:
                return ("invalidcode")

        else:
            return ("nocode")
    

    def restart(self):
        #
        # Restart the system
        #
        os.system("shutdown -r now")

    def shutdown(self):
        #
        # Shutdown the system
        #
        os.system("shutdown -h now")

