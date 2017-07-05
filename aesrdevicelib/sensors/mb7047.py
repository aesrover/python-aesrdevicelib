from . import i2c_device
import time

class MB7047(i2c_device.I2cDevice):
    '''Library for the MaxBotix 12CXL-MaxSonar-WR Sensor'''
    
    _DEFAULT_I2C_ADDRESS = 0x70
    
    _REG_START_WRITE = 81    # Register address to take a measurement
    _REG_START_MEASURE = 0   # Register address to read back measurement
    
    _BAD_VALUES = [255]      # The bad values that should cause a reading to be
                             # discarded
    
    _MAX_LOOPS = 10          # Maximum number of bad value loops that 
                             # can be done before raising an error
    
    loopNumber = 0           # The number of bad value loops that have been done
    
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(MB7047, self).__init__(i2cAddress, *args, **kwargs)
    
    # Read distance in centimeters        
    def readCM(self):
        if self.loopNumber > (self._MAX_LOOPS - 1):
            raise ValueError("The sensor has returned a bad value ("
                                + str(self._BAD_VALUES) + ") more than "
                                + str(self._MAX_LOOPS) + "times")
        
        # Signal device to take measurement
        self.write_byte(self._REG_START_WRITE)
        
        # Wait 1/10th of a Second to allow device to complete the measurement
        time.sleep(0.1)
        
        # Read measurement data from device
        data = self.read_i2c_block_data(self._REG_START_MEASURE)
        
        # Remove leading bit from first byte, bit shift,
        # and add to calculate distance
        value = ((data[0] & 0b1111111)<<8) + data[1]
        
        for ii in self._BAD_VALUES:
            if value == ii:
                self.loopNumber += 1
                value = self.readCM()
                break
        
        self.loopNumber = 0
        return value
    
    # Main read function
    def read(self, *args, **kwargs):
        return self.readCM(*args, **kwargs)
        
    def readM(self, *args, **kwargs):
        return (self.readCM(*args, **kwargs))/100
