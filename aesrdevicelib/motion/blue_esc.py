from ..sensors import i2c_device


class BlueESC_I2C(i2c_device.I2cDevice):
    """Library for the Blue Robotics BlueESC"""
    _DEFAULT_I2C_ADDRESS = 0x29
    _THROTTLE_REGISTER = 0x00

    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super().__init__(i2cAddress, *args, **kwargs)

    def start(self):
        self.write_word_data(self._THROTTLE_REGISTER, 0)

    def set_power(self, power):
        self.write_word_data(self._THROTTLE_REGISTER, power)

    def start_power(self, speed):
        self.start()
        self.set_power(speed)
