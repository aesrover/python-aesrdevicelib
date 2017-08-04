from .. import i2c_device


class TCA9548A(i2c_device.I2cDevice):
    '''Library for the Adafruit TCA9548A Multiplexer'''

    _DEFAULT_I2C_ADDRESS = 0x71

    def __init__(self, i2c_address=_DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(TCA9548A, self).__init__(i2c_address, *args, **kwargs)

    def select_channel(self, c: int):
        if c > 7 or c < 0:
            raise ValueError("Channel out of range [0,7]")

        # Write channel to TCA twice (as once didn't seem to be reliable):
        self.write_byte(1 << c)
        self.write_byte(1 << c)
