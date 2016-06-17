import smbus
from . import sensor
import time

class MB7047(sensor.Sensor):
    '''Library for the MaxBotix 12CXL-MaxSonar-WR Sensor'''
    
    _DEFAULT_I2C_ADDRESS = 112
    
    _REG_START_WRITE = 81    # register address to take a measurement
    _REG_START_MEASURE = 0   # register address to read back measurement
    
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(MB7047, self).__init__(i2cAddress, *args, **kwargs)
    
    # Read depth in centimeters        
    def readCM(self):
        # Write to sensor to start measurement
        self.bus.write_byte_data(self.i2cAddress, self._REG_START_WRITE, 0)
        
        # Wait 1/20th of a Second to allow device to complete the measurement
        time.sleep(0.05)
        
        # Read 16bit depth from device
        depth = self.bus.read_word_data(self.i2cAddress, self._REG_START_MEASURE)
        
        return depth
        
    # Main read function
    def read(self, *args, **kwargs):
        return self.readCM(*args, **kwargs)
        
    def readM(self, *args, **kwargs):
        return (self.readCM(*args, **kwargs))/100