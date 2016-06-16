import smbus
from . import sensor

class ADS1115(sensor.Sensor):
    
    _DEFAULT_I2C_ADDRESS = 0x48
    
    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(ADS1115, self).__init__(self, *args, **kwargs)
        
        new_config = 0b0100001110000011
        # This config: Enables continuos reading, Disables comparator,
        # Sets the analog voltage range to 0 - 6V, and sets 
        
        # Write two bytes to the config register 
        self.bus.write_word_data(self.i2cAddress, 0x01, new_config)

    
    def read(self):                
        # Read two bytes from register 00, the ADC value
        value = self.bus.read_word_data(self.i2cAddress, 0x00) & 0xFFFF
        # Swap byte order from little endian to big endian
        value = ((value & 0xFF) << 8) | (value >> 8)
        return value
