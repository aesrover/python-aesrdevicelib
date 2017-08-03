from ..sensors import i2c_device


class TCA9548A(i2c_device.I2cDevice):
    '''Library for the Adafruit TCA9548A Multiplexer'''

    _DEFAULT_I2C_ADDRESS = 0x71

    def __init__(self, i2c_address=_DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(TCA9548A, self).__init__(i2c_address, *args, **kwargs)

    def tcaselect(self, i):
        if i > 7:
            return

        self.write_byte(1 << i)
        self.write_byte(1 << i)
