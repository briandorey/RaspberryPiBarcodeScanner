#!/usr/bin/env python

try:
    import smbus
except ImportError:
    raise ImportError("python-smbus not found. Install with 'sudo apt-get install python-smbus'")
import re


class LTC2943_1:
    """ Functions for controlling the LTC2943_1 battery monitor IC"""

    global bus
    
    # I2C Address and Register Locations
    I2C_ADDRESS=0x64
    I2C_BUS = 1

    STATUS = 0x00
    CONTROL = 0x01
    ACCUMULATED_CHARGE_MSB = 0x02
    ACCUMULATED_CHARGE_LSB = 0x03
    CHARGE_THRESHOLD_HIGH_MSB = 0x04
    CHARGE_THRESHOLD_HIGH_LSB = 0x05
    CHARGE_THRESHOLD_LOW_MSB = 0x06
    CHARGE_THRESHOLD_LOW_LSB = 0x07
    VOLTAGE_MSB = 0x08
    VOLTAGE_LSB = 0x09
    VOLTAGE_THRESHOLD_HIGH_MSB = 0x0A
    VOLTAGE_THRESHOLD_HIGH_LSB = 0x0B
    VOLTAGE_THRESHOLD_LOW_MSB = 0x0C
    VOLTAGE_THRESHOLD_LOW_LSB = 0x0D
    CURRENT_MSB = 0x0E
    CURRENT_LSB = 0x0F
    CURRENT_THRESHOLD_HIGH_MSB = 0x10
    CURRENT_THRESHOLD_HIGH_LSB = 0x11
    CURRENT_THRESHOLD_LOW_MSB = 0x12
    CURRENT_THRESHOLD_LOW_LSB = 0x13
    TEMPERATURE_MSB = 0x14
    TEMPERATURE_LSB = 0x15
    TEMPERATURE_THRESHOLD_HIGH = 0x16
    TEMPERATURE_THRESHOLD_LOW = 0x17

    def get_smbus(self):
        # detect i2C port number and assign to i2c_bus
        i2c_bus = 0
        for line in open('/proc/cpuinfo').readlines():
            m = re.match('(.*?)\s*:\s*(.*)', line)
            if m:
                (name, value) = (m.group(1), m.group(2))
                if name == "Revision":
                    if value[-4:] in ('0002', '0003'):
                        i2c_bus = 0
                    else:
                        i2c_bus = 1
                    break
        try:        
            return smbus.SMBus(i2c_bus)
        except IOError:
                print ("Could not open the i2c bus.")

    def __init__(self):
        self.bus = self.get_smbus()


    def set_control(self, config):
        x = [config]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CONTROL, x)
        return

    def set_charge_threshold_high(self, value):
        low = [value]
        high = [(value & 0xff00) >> 8]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CHARGE_THRESHOLD_HIGH_LSB, low)
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CHARGE_THRESHOLD_HIGH_MSB, high)
        return

    def set_charge_threshold_low(self, value):
        low = [value]
        high = [(value & 0xff00) >> 8]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CHARGE_THRESHOLD_LOW_LSB, low)
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CHARGE_THRESHOLD_HIGH_MSB, high)
        return

    def set_voltage_threshold_high(self, value):
        low = [value]
        high = [(value & 0xff00) >> 8]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.VOLTAGE_THRESHOLD_HIGH_LSB, low)
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.VOLTAGE_THRESHOLD_HIGH_MSB, high)
        return

    def set_voltage_threshold_low(self, value):
        low = [value]
        high = [(value & 0xff00) >> 8]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.VOLTAGE_THRESHOLD_LOW_LSB, low)
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.VOLTAGE_THRESHOLD_LOW_MSB, high)
        return

    def set_current_threshold_high(self, value):
        low = [value]
        high = [(value & 0xff00) >> 8]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CURRENT_THRESHOLD_HIGH_LSB, low)
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CURRENT_THRESHOLD_HIGH_MSB, high)
        return

    def set_current_threshold_low(self, value):
        low = [value]
        high = [(value & 0xff00) >> 8]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CURRENT_THRESHOLD_LOW_LSB, low)
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.CURRENT_THRESHOLD_LOW_MSB, high)
        return

    def set_temperature_threshold_high(self, value):
        x = [value]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.TEMPERATURE_THRESHOLD_HIGH, x)
        return

    def set_temperature_threshold_low(self, value):
        x = [value]
        self.bus.write_i2c_block_data(self.I2C_ADDRESS, self.TEMPERATURE_THRESHOLD_LOW, x)
        return
    
    def get_data(self):
        out = self.bus.read_i2c_block_data(self.I2C_ADDRESS, 0x00, 24)
        return out

    def get_voltage(self):
        datablock = self.bus.read_i2c_block_data(self.I2C_ADDRESS, self.VOLTAGE_MSB, 2)
        t = ((datablock[0]) << 8) | datablock[1]
        out = ((float(t) / 65535.0) * 23.6) + 0.2 
        return out

    def parse_control(self):        
        t = datablock[self.CONTROL]
        return t

    def parse_status(self, datablock):
        t = datablock[self.STATUS]
        return t

    def parse_voltage(self, datablock):
        t = ((datablock[self.VOLTAGE_MSB]) << 8) | datablock[self.VOLTAGE_LSB]
        out = ((float(t) / 65535.0) * 23.6) + 0.2        
        return out

    def parse_current(self, datablock):
        t = ((datablock[self.CURRENT_MSB]) << 8) | datablock[self.CURRENT_LSB]
        out = ((float(t - 32767) / 32767.0) * 1.3) / -1  
        return out







