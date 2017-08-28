from .. import i2c_device
from .pca9685 import PCA9685
from ..base.motor import Thruster


class BlueESC_I2C(i2c_device.I2cDevice, Thruster):
    """Library for the Blue Robotics BlueESC"""
    _DEFAULT_I2C_ADDRESS = 0x29
    _THROTTLE_REGISTER = 0x00

    def __init__(self, v, a, i2cAddress= _DEFAULT_I2C_ADDRESS, *args, **kwargs):
        super().__init__(i2cAddress, *args, **kwargs)
        Thruster.__init__(self, v, a)

    def start(self):
        self.write_word_data(self._THROTTLE_REGISTER, 0)

    def _set_motor_power(self, p: float):
        p *= 32767
        p = round(p)
        self.write_word_data(self._THROTTLE_REGISTER, p)

    def start_power(self, power: float):
        self.start()
        self.set_power(power)


class BlueESC_PCA9685(Thruster):
    # PCA9685 PWM values for BlueESC (full rev, init, full fwd)
    BLUEESC_PWM_FREQS = {400: (2005, 2685, 2735, 2785, 3450), 350: (1760, 2370, 2400, 2455, 3050), 300: (1505, 2015, 2050, 2086, 2595)}

    def __init__(self, v, a, channel: int, pca9685: PCA9685=None, pwm_freq: int=300,
                 **kwargs: "PCA9685 kwargs (if not supplied)"):
        self.channel = channel
        super().__init__(v, a)

        if pwm_freq not in self.BLUEESC_PWM_FREQS:
            raise ValueError("PWM Frequency must be one of {}.".format(list(self.BLUEESC_PWM_FREQS.keys())))

        if pca9685 is None:
            pca9685 = PCA9685(**kwargs)
            pca9685.set_pwm_freq(pwm_freq)
        self.pca = pca9685

        freqs = self.BLUEESC_PWM_FREQS[pwm_freq]
        self.full_bck = freqs[0]
        self.min_bck = freqs[1]
        self.mid = freqs[2]
        self.min_fwd = freqs[3]
        self.full_fwd = freqs[4]

    def set_pwm(self, on, off):
        """ Wrapper function of `pca.set_pwm`. Fills in channel number. """
        self.pca.set_pwm(self.channel, on, off)

    def enable(self):
        """ Send initialization to ESC. Must be run first, or after a call to `disable`. """
        self.set_pwm(0, self.mid)

    def _set_motor_power(self, p: float):
        """ Set the power of the BlueESC (in the range of -1,1). """
        p_val = self.mid
        if p < 0:
            p_val = float(p) * (self.min_bck - self.full_bck) + self.min_bck
        elif p > 0:
            p_val = float(p) * (self.full_fwd - self.min_fwd) + self.min_fwd
        p_val = round(p_val)

        self.set_pwm(0, p_val)

    def stop(self):
        """ Stop the BlueESC (will stay initialized). """
        self.set_power(0)

    def disable(self):
        """ Stop and disable the BlueESC. """
        self.stop()
        self.set_pwm(0, 0)  # Disable PWM
