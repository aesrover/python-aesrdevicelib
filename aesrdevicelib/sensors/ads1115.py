from .. import i2c_device
import time


class ADS1115(i2c_device.I2cDevice):
    '''Library for the Adafruit ADS1115 ADC'''

    _DEFAULT_I2C_ADDRESS = 0x48
    FS = 6.144

    def __init__(self, i2cAddress=_DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(ADS1115, self).__init__(i2cAddress, *args, **kwargs)

    def read(self):
        dataRate = 128
        # Write two bytes to the config register
        self.write_word_data(0x01, 0b0100000010000011)
        # This config: Enables continuos conversion, Disables comparator,
        # Sets the analog voltage range to 0 - 6V, and much more!
        # https://cdn-shop.adafruit.com/datasheets/ads1115.pdf (18-19)

        # Wait for the ADC sample to finish based on the sample rate plus a
        # small offset to be sure (0.1 millisecond).
        time.sleep(1.0/dataRate+0.0001)

        # Read two bytes from register 00, the ADC value
        value = self.read_i2c_block_data(0x00, 2)
        # Assemble bytes
        intvalue = value[0] * 256 + value[1]
        return intvalue

    def asVolt(self, adc):
        return self.FS * adc / (pow(2, 15) - 1)

    def readVolt(self, *args, **kwargs):
        # Converts to a voltage
        return self.asVolt(self.read(*args, **kwargs))
