import smbus

class Sensor(object):
    def __init__(self, i2cAddress, bus= 1):
        self.bus = smbus.SMBus(bus)
        self.i2cAddress = i2cAddress
        
        # Test if device is connected:
        self.bus.read_byte(i2cAddress)