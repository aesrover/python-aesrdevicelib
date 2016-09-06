import smbus


class Sensor(object):
    def __init__(self, i2cAddress, bus=1):
        self.bus = smbus.SMBus(bus)
        self.i2cAddress = i2cAddress

        # Test if device is connected by transmitting just the slave address
        # and checking for an ACK from the device:
        self.bus.write_quick(i2cAddress)
