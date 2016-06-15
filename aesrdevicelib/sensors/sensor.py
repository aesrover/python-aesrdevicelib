import smbus

class Sensor(object):
    def __init__(self, i2cAddress, bus):
        self.bus = smbus.SMBus(bus)
        self.i2cAddress = i2cAddress