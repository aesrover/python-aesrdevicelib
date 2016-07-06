from . import sensor
import time


class BlueESC(sensor.Sensor):
    """Library for the Blue Robotics BlueESC"""
    _DEFAULT_I2C_ADDRESS = 0x29
    _THROTTLE_REGISTER = 0x00

    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super(BlueESC, self).__init__(i2cAddress, *args, **kwargs)

    def start(self):
        self.bus.write_word_data(self._DEFAULT_I2C_ADDRESS, self._THROTTLE_REGISTER, 0)

    def setPower(self, power):
        self.bus.write_word_data(self._DEFAULT_I2C_ADDRESS, self._THROTTLE_REGISTER, power)

    def startPower(self, speed):
        self.startup()
        self.setPower(speed)
