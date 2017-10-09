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
    def __init__(self):
        self.curr_tick = 0

    def stop(self):
        """ Stop the motor. """
        raise NotImplementedError

    def is_moving(self) -> bool:
        """ Returns bool to signal if motor is moving. """
        raise NotImplementedError

    def _move_tick(self, rel_t, p=None):
        """ Move by some number of ticks, at speed p. To be implemented by subclasses. """
        raise NotImplementedError

    def move_rel_tick(self, rel_t, p=None):
        """ Move rel_t ticks (relatively), at speed p. Use default p if not given. """
        self.curr_tick += rel_t
        self._move_tick(rel_t, p)

    def move_abs_tick(self, abs_t, p=None):
        """ Move to an absolute tick position, abs_t, at speed p. Use default p if not given. """
        rel_t = abs_t - self.curr_tick
        self.move_rel_tick(rel_t, p)

    def get_curr_tick(self):
        return self.curr_tick
