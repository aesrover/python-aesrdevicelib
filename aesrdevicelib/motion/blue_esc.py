from ..sensors import i2c_device
from .pca9685 import PCA9685


class BlueESC_I2C(i2c_device.I2cDevice):
    """Library for the Blue Robotics BlueESC"""
    _DEFAULT_I2C_ADDRESS = 0x29
    _THROTTLE_REGISTER = 0x00

    def __init__(self, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super().__init__(i2cAddress, *args, **kwargs)

    def start(self):
        self.write_word_data(self._THROTTLE_REGISTER, 0)

    def set_power(self, power: float):
        if power < -1 or power > 1:
            raise ValueError("Power must be within [-1,1].")
        power *= 32767
        power = round(power)
        self.write_word_data(self._THROTTLE_REGISTER, power)

    def start_power(self, power: float):
        self.start()
        self.set_power(power)


class BlueESC_PCA9685():
    # PCA9685 PWM values for BlueESC (full rev, init, full fwd)
    BLUEESC_PWM_FREQS = {400: (2005, 2735, 3450), 350: (1760, 2400, 3050), 300: (1505, 2050, 2595)}

    def __init__(self, channel: int, pca9685: PCA9685=None, pwm_freq: int=300,
                 **kwargs: "PCA9685 kwargs (if not supplied)"):
        self.channel = channel

        if pca9685 is None:
            pca9685 = PCA9685(**kwargs)
        self.pca = pca9685

        if pwm_freq not in self.BLUEESC_PWM_FREQS:
            raise ValueError("PWM Frequency must be one of {}.".format(list(self.BLUEESC_PWM_FREQS.keys())))
        self.pca.set_pwm_freq(pwm_freq)

        freqs = self.BLUEESC_PWM_FREQS[pwm_freq]
        self.min = freqs[0]
        self.mid = freqs[1]
        self.max = freqs[2]

    def set_pwm(self, on, off):
        """ Wrapper function of `pca.set_pwm`. Fills in channel number. """
        self.pca.set_pwm(self.channel, on, off)

    def enable(self):
        """ Send initialization to ESC. Must be run first, or after a call to `disable`. """
        self.set_pwm(0, self.mid)

    def set_power(self, pwr: float):
        """ Set the power of the BlueESC (in the range of -1,1). """
        if pwr > 1 or pwr < -1:
            raise ValueError("Power must be within [-1,1].")

        pwr_val = self.mid
        if pwr < 0:
            pwr_val = float(pwr) * (self.mid - self.min) + self.mid
        elif pwr > 0:
            pwr_val = float(pwr) * (self.max - self.mid) + self.mid
        pwr_val = round(pwr_val)

        self.set_pwm(0, pwr_val)

    def stop(self):
        """ Stop the BlueESC (will stay initialized). """
        self.set_power(0)

    def disable(self):
        """ Stop and disable the BlueESC. """
        self.stop()
        self.set_pwm(0, 0)  # Disable PWM
