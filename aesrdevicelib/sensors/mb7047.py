from . import sensor
import time

class MB7047(sensor.Sensor):
    '''Library for the MaxBotix 12CXL-MaxSonar-WR Sensor'''
    
    _DEFAULT_I2C_ADDRESS = 0x70
    
    _REG_START_WRITE = 81    # register address to take a measurement
    _REG_START_MEASURE = 0   # register address to read back measurement
    
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(MB7047, self).__init__(i2cAddress, *args, **kwargs)
    
    # Read distance in centimeters        
    def readCM(self):
        # Signal device to take measurement
        self.bus.write_byte(self.i2cAddress, self._REG_START_WRITE)
        
        # Wait 1/10th of a Second to allow device to complete the measurement
        time.sleep(0.1)
        
        # Read measurement data from device
        data = self.bus.read_i2c_block_data(self.i2cAddress
                                            , self._REG_START_MEASURE)
        
        # Remove leading bit from first byte, bit shift,
        # and add to calculate distance
        return ((data[0] & 0b1111111)<<8) + data[1]
        
    # Main read function
    def read(self, *args, **kwargs):
        return self.readCM(*args, **kwargs)
        
    def readM(self, *args, **kwargs):
        return (self.readCM(*args, **kwargs))/100
