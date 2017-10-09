from typing import Tuple


class Motor:
    def _set_motor_power(self, p: float):
        raise NotImplementedError

    def set_power(self, p: float):
        if abs(p) > 1:
            raise ValueError("Power value needs to be in range [-1,1].")
        return self._set_motor_power(p)


class Thruster(Motor):
    def __init__(self, v: Tuple[float, float], a: float):
        self.v = v
        self.a = a

    def _set_motor_power(self, p: float):
        raise NotImplementedError


class ControlledMotor(Motor):
    """ A motor capable of relative movement by tick number. """

    def move_ticks(self, t, p=None):
        """ Move t ticks, at speed p. Use default p if not given. """
        raise NotImplementedError
